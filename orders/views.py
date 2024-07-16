import os

from concurrent.futures import ThreadPoolExecutor

from dal import autocomplete
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q
from django.db.models.functions import Lower
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.http import FileResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from sorl.thumbnail import get_thumbnail

from .forms import OrderForm, OrderServiceForm, AttachmentForm, AttachmentFormSet
from .models import Attachment, Order, Region, PriorityChoices, OrderService
from .utils import get_report
from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from customers.forms import CustomerForm, AdditionalAddressForm
from customers.models import Customer, AdditionalAddress
from devices.forms import DeviceForm
from devices.models import Device
from employees.models import Employee
from order_management.views import EmployeesOrdersList, OrderListViewBase
from order_review.models import OrderReview
from orders.utils import map_choices_int_to_str
from services.models import Brand, Model, Service


def get_services(request):
    result = []
    for key, value in request.session.items():
        if key.isdigit():
            service_id = value['service']
            if service_id:
                service_instance = get_object_or_404(Service, pk=int(value['service']))
            else:
                service_instance = None

            order_service = OrderService(
                id=int(key),
                service=service_instance,
                name=value['name'],
                price_net=float(value['price_net']),
                quantity=int(value['quantity']),
                from_session=True,
            )
            result.append(order_service)
    return result


class CustomerAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Customer.objects.none()

        qs = Customer.objects.all()

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(user__first_name__icontains=self.q) |
                Q(user__last_name__icontains=self.q) |
                Q(tax__icontains=self.q) |
                Q(billing_city__icontains=self.q) |
                Q(billing_street__icontains=self.q) |
                Q(phone_number__icontains=self.q)
            )

        return qs.order_by(Lower('name'))


class ExecutorAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Employee.objects.none()

        qs = Employee.objects.select_related()

        if self.q:
            qs = qs.filter(
                Q(user__first_name__icontains=self.q) |
                Q(user__last_name__icontains=self.q)
            )

        return qs.order_by(Lower('user__first_name'))


class AddressAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return AdditionalAddress.objects.none()

        customer_id = self.request.session.get('customer_id')
        if customer_id:
            qs = AdditionalAddress.objects.filter(customer_id=customer_id, is_active=True)

            if self.q:
                qs = qs.filter(
                    Q(city__icontains=self.q) |
                    Q(street__icontains=self.q)
                )

            return qs.order_by(Lower('city'))
        return AdditionalAddress.objects.none()


class DeviceAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Device.objects.none()

        qs = Device.objects.all()

        if self.q:
            qs = qs.filter(
                Q(serial_number__icontains=self.q)
            )

        return qs.order_by(Lower('brand__name'))


class ServiceAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Service.objects.none()

        active_brands = Brand.objects.filter(is_active=True)
        qs = Service.objects.filter(is_active=True, device_brand__in=active_brands)
        qs = qs.filter(Q(device_model__isnull=True) | Q(device_model__is_active=True))

        service_filter_by_brand_id = self.request.session.get('service_filter_by_brand', '')
        service_filter_by_model_id = self.request.session.get('service_filter_by_model', '')

        if service_filter_by_brand_id and service_filter_by_brand_id != 'All':
            qs = qs.filter(device_brand__id=service_filter_by_brand_id)
        if service_filter_by_model_id and service_filter_by_model_id != 'All':
            qs = qs.filter(device_model__id=service_filter_by_model_id)

        if self.q:
            qs = qs.filter(
                Q(device_brand__name__icontains=self.q) |
                Q(device_model__name__icontains=self.q) |
                Q(name__icontains=self.q) |
                Q(description__icontains=self.q)
            )

        return qs.order_by(Lower('device_model__name')).order_by(Lower('device_brand__name'))


class AttachmentDetails(EmployeeRequiredMixin, View):
    def get(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        if attachment.image:
            return HttpResponse(attachment.image, content_type="image/png")
        else:
            return FileResponse(open(attachment.file.path, 'rb'), content_type='application/pdf')


class AttachmentDelete(EmployeeRequiredMixin, View):
    def get(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        attachment.delete()

        order_id = request.GET.get('order_id')
        atts = Attachment.objects.filter(order__id=order_id)
        attachments = {}
        for att in atts:
            if att.image:
                attachments[att.id] = {'image': get_thumbnail(att.image.name, '300x300', crop='center', quality=20)}
            else:
                import os
                attachments[att.id] = {'filename': os.path.basename(att.file.name)}

        return render(request, 'orders/attachments_list.html', {'attachments': attachments})


class OrderUpdateAPIView(EmployeeRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        selected_type = request.POST.get('selected_type')
        selected_value = request.POST.get('selected_value')

        if selected_type == 'executor' and selected_value:
            if selected_value and selected_value != '-1':
                employee = get_object_or_404(Employee, pk=selected_value)
            if selected_value == '-1':
                employee = None
            order.executor = employee

        elif selected_type == 'region' and selected_value:
            if selected_value and selected_value != '-1':
                region = get_object_or_404(Region, pk=selected_value)
            if selected_value == '-1':
                region = None
            order.region = region

        elif selected_type == 'priority' and selected_value:
            if selected_value in [str(choice.value) for choice in PriorityChoices]:
                order.priority = selected_value

        order.save()

        return JsonResponse({'status': 200, 'success': 'true'})


class OrderList(EmployeeRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders_list.html'
    paginate_by = 10

    def get_template_names(self):
        search_query = self.request.GET.get('search', False)
        if search_query or search_query == '':
            return ['orders/orders_list_table.html']
        return super().get_template_names()

    def get_queryset(self):
        orders = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        order_by = self.request.GET.get('order_by', '-id')
        customer_id = self.request.GET.get('customer_id')
        device_id = self.request.GET.get('device_id')

        if device_id and device_id != 'None':
            orders = orders.filter(device__id=device_id)

        if customer_id and customer_id != 'None':
            orders = orders.filter(customer__id=customer_id)

        if search_query:
            orders = orders.filter(
                Q(id__contains=search_query) |
                Q(customer__name__icontains=search_query) |
                Q(invoice_number__icontains=search_query) |
                Q(device__serial_number__icontains=search_query)
            )
        orders = orders.order_by(order_by)

        return orders

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        order_by = self.request.GET.get('order_by', '-id')
        customer_id = self.request.GET.get('customer_id')
        device_id = self.request.GET.get('device_id')

        context['order_by'] = order_by
        context['page_objs'] = context['page_obj']

        if customer_id and customer_id != 'None':
            self.request.session['customer_id'] = customer_id
            customer = get_object_or_404(Customer.objects.values('id', 'name'), pk=customer_id)
            context['customer'] = customer

        if device_id and device_id != 'None':
            device = get_object_or_404(
                Device.objects.values('id', 'brand', 'model', 'serial_number'),
                pk=self.request.GET.get('device_id'),
            )
            context['device'] = device

        del context['page_obj']

        return context


class OrderUpdate(EmployeeRequiredMixin, View):
    model = Order
    template_name = 'orders/order_update.html'
    order_form_class = OrderForm
    customer_form_class = CustomerForm
    address_form_class = AdditionalAddressForm
    device_form_class = DeviceForm
    order_service_form_class = OrderServiceForm
    attachment_formset = AttachmentFormSet

    def get_context_data(self, **kwargs):
        order_id = kwargs.get('pk')
        customer_id = kwargs.get('customer_id')
        payer_id = kwargs.get('payer_id')
        address_id = kwargs.get('address_id')
        device_id = kwargs.get('device_id')
        attachments = None

        if order_id:
            order_instance = get_object_or_404(self.model.objects.select_related(), pk=order_id)
            self.request.session['customer_id'] = order_instance.customer.id
            atts = order_instance.attachment_set.all()
            attachments = {}
            for att in atts:
                if att.image:
                    attachments[att.id] = {'image': get_thumbnail(att.image.name, '300x300', crop='center', quality=20)}
                else:
                    attachments[att.id] = {'filename': os.path.basename(att.file.name)}

        else:
            order_instance = None
            self.request.session['customer_id'] = None

        if customer_id:
            self.request.session['customer_id'] = customer_id
            customer_instance = get_object_or_404(Customer, pk=customer_id)
            if order_instance:
                order_instance.customer = customer_instance
                if not order_instance.phone_number:
                    order_instance.phone_number = customer_instance.phone_number

        else:
            customer_instance = None

        if not customer_id and not order_id:
            self.request.session['customer_id'] = None

        if payer_id:
            payer_instance = get_object_or_404(Customer, pk=payer_id)
            if order_instance:
                order_instance.payer = payer_instance
        else:
            payer_instance = None

        if address_id == 'null':
            if order_instance:
                order_instance.additional_address = None
        if address_id:
            address_instance = get_object_or_404(AdditionalAddress, pk=address_id)
            if order_instance:
                order_instance.additional_address = address_instance
        else:
            address_instance = None

        if device_id:
            device_instance = get_object_or_404(Device, pk=device_id)
            if order_instance:
                order_instance.device = device_instance
        else:
            device_instance = None

        if order_instance:
            customer_instance = get_object_or_404(Customer, pk=order_instance.customer.id)

            if not order_instance.phone_number:
                setattr(order_instance, 'phone_number', '')

            if customer_instance:
                for attr, value in customer_instance.__dict__.items():
                    if value is None and attr == 'phone_number':
                        setattr(order_instance.customer, attr, '')
                        continue
                    if value is None:
                        setattr(customer_instance, attr, '---')
            if order_instance.customer:
                for attr, value in order_instance.customer.__dict__.items():
                    if value is None and attr == 'phone_number':
                        setattr(order_instance.customer, attr, '')
                        continue
                    if value is None:
                        setattr(order_instance.customer, attr, '---')
            if order_instance.payer:
                for attr, value in order_instance.payer.__dict__.items():
                    if value is None and attr == 'phone_number':
                        setattr(order_instance.payer, attr, '')
                        continue
                    if value is None:
                        setattr(order_instance.payer, attr, '---')
            if order_instance.additional_address:
                for attr, value in order_instance.additional_address.__dict__.items():
                    if value is None:
                        setattr(order_instance.additional_address, attr, '---')

            order_form = self.order_form_class(instance=order_instance)
            order_services = order_instance.services.filter(is_active=True)
        else:
            order_services = []
            initial_data = {
                'customer': customer_instance,
                'payer': payer_instance,
                'additional_address': address_instance,
                'device': device_instance,
            }
            order_form = self.order_form_class(initial=initial_data)

        total_summary = sum(service.quantity * service.price_net for service in order_services)

        if order_instance:
            for attr, value in order_instance.__dict__.items():
                if value is None and attr == 'phone_number':
                    setattr(customer_instance, attr, '')
                if value is None:
                    setattr(customer_instance, attr, '---')

        context = {
            'order_instance': order_instance,
            'customer_instance': customer_instance,
            'order_form': order_form,
            'customer_form': self.customer_form_class(),
            'address_form': self.address_form_class(),
            'device_form': self.device_form_class(),
            'order_service_form': self.order_service_form_class(),
            'attachment_formset': self.attachment_formset(queryset=Attachment.objects.none()),
            'attachments': attachments,
            'order_services': order_services,
            'total_summary': total_summary,
            'brands': Brand.objects.filter(is_active=True),
            'models': Model.objects.filter(is_active=True),
        }

        return context

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            order_instance = self.model.objects.select_related().filter(pk=kwargs.get('pk')).first()
        else:
            order_instance = self.model()
            order_instance.user_intake = self.request.user.employee.first()

        if not order_instance.phone_number and order_instance.customer:
            order_instance.phone_number = order_instance.customer.phone_number

        request_data = request.POST.copy()
        address_id = request_data.pop('additional_address', None)
        if address_id:
            address_id = address_id.pop()

        order_form = self.order_form_class(request_data, instance=order_instance)

        for file in request.FILES:
            att = AttachmentForm(files={file.split('-')[2]: request.FILES[file]})
            if att.is_valid():
                inst = att.save(commit=False)
                inst.order = order_instance
                inst.save()

        if order_form.is_valid():
            order_instance = order_form.save(commit=False)
            if address_id:
                address_instance = get_object_or_404(AdditionalAddress, pk=address_id)
                customer_id = request_data.get('customer')
                self.request.session['customer_id'] = customer_id
                customer_instance = get_object_or_404(Customer, pk=customer_id)
                if address_instance in customer_instance.additionaladdress_set.all():
                    order_instance.additional_address = address_instance
                else:
                    context = self.get_context_data(**kwargs)

                    return render(request, self.template_name, context)

            order_instance.save()

            office_employees_ids = Employee.objects.filter(department__lte=2)
            if order_instance.status in [2, 3, 4, 5]:
                for employee in office_employees_ids:
                    order_review = OrderReview.objects.filter(order_id=order_instance.id, user_id=employee.user.id)
                    if not order_review:
                        OrderReview(order_id=order_instance.id, user_id=employee.user.id).save()

            services_list = get_services(request)
            if services_list:
                for service in services_list:
                    service.id = None
                    service.save()
                    order_instance.services.add(service)

            return HttpResponseRedirect(reverse_lazy('orders:order_details', kwargs={'pk': order_instance.id}))
        else:
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        self.request.session.pop('service_filter_by_brand', None)
        self.request.session.pop('service_filter_by_model', None)

        services = get_services(request)
        for service in services:
            self.request.session.pop(str(service.id), None)

        return render(
            request,
            self.template_name,
            context=self.get_context_data(
                pk=kwargs.get('pk'),
                customer_id=request.GET.get('customer_id'),
                payer_id=request.GET.get('payer_id'),
                address_id=request.GET.get('address_id'),
                device_id=request.GET.get('device_id'),
            )
        )


class OrderDetails(OrderUpdate):
    template_name = 'orders/order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for form in context.values():
            if issubclass(type(form), ModelForm):
                for field in form.fields.values():
                    field.disabled = True

        return context


class CustomerDetails(EmployeeRequiredMixin, View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        for attr, value in customer.__dict__.items():
            if value is None and attr != 'phone_number':
                setattr(customer, attr, '---')
        request.session['customer_id'] = customer.id
        order_form = OrderForm
        context = {'customer': customer, 'order_form': order_form}

        return render(request, 'orders/customer_details.html', context=context)


class CustomerCreateModal(EmployeeRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm

    def form_valid(self, form):
        customer_instance = form.save()
        customer_id = customer_instance.id

        return JsonResponse({'status': 201, 'customer_id': customer_id})


class AddressDetails(EmployeeRequiredMixin, DetailView):
    model = AdditionalAddress
    template_name = 'orders/address_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        for attr, value in context['additionaladdress'].__dict__.items():
            if value is None:
                setattr(context['additionaladdress'], attr, '---')
        return context


class AddressForm(EmployeeRequiredMixin, View):
    def get(self, request, customer_id):
        self.request.session['customer_id'] = customer_id
        order_form = OrderForm()
        context = {'order_form': order_form}

        return render(request, 'orders/address_form.html', context=context)


class AddressCreateModal(EmployeeRequiredMixin, View):
    def post(self, request):
        address_form = AdditionalAddressForm(request.POST)
        if address_form.is_valid():
            address_instance = address_form.save()
            return JsonResponse({'status': 201, 'address_id': address_instance.id})
        return JsonResponse({'status': 400})


class DeviceCreateModal(EmployeeRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm

    def form_invalid(self, form):
        return JsonResponse({'status': 400, 'errors': form.errors.as_ul()})

    def form_valid(self, form):
        device_instance = form.save()
        device_id = device_instance.id

        return JsonResponse({'status': 201, 'device_id': device_id})


class ServicesFiler(EmployeeRequiredMixin, ListView):
    model = Service

    def get_queryset(self):
        brand_id = self.request.GET.get('brand_id')
        model_id = self.request.GET.get('model_id')

        filtered_services = super().get_queryset()

        if brand_id != 'All':
            filtered_services = filtered_services.filter(device_brand__id=brand_id)
        if model_id != 'All':
            filtered_services = filtered_services.filter(device_model__id=model_id)

        return filtered_services

    def render_to_response(self, context, **response_kwargs):
        self.request.session['service_filter_by_brand'] = self.request.GET.get('brand_id')
        self.request.session['service_filter_by_model'] = self.request.GET.get('model_id')

        options = []
        for service in context['object_list']:
            options.append({
                'id': service.id,
                'name': str(service),
            })

        return JsonResponse(options, safe=False)


class ServiceDetails(EmployeeRequiredMixin, DetailView):
    model = Service

    def render_to_response(self, context, **response_kwargs):
        service = context['object']

        return JsonResponse({
            'name': service.name,
            'price_net': service.price_net,
            'quantity': 1
        })

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)


class OrderServicesList(EmployeeRequiredMixin, ListView):
    def get(self, request):
        order_id = request.GET.get('order_id')
        services_data = get_services(request)

        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            services_data += list(order.services.filter(is_active=True))

        total_summary = sum(service.quantity * service.price_net for service in services_data)
        context = {
            'services': services_data,
            'total_summary': total_summary,
        }

        return render(request, 'orders/order_services_list.html', context=context)


class OrderServiceCreate(EmployeeRequiredMixin, CreateView):
    model = OrderService
    form_class = OrderServiceForm

    def form_invalid(self, form):
        return JsonResponse({'status': 400})

    def form_valid(self, form):
        obj = form.save(commit=False)
        service_ids = [int(key) for key in self.request.session.keys() if key.isdigit()]

        if service_ids:
            next_service_id = max(service_ids) + 1
        else:
            next_service_id = 1

        obj.id = next_service_id
        self.request.session[str(next_service_id)] = model_to_dict(obj)

        return JsonResponse({'status': 201})


class OrderServiceDetails(EmployeeRequiredMixin, View):
    def get(self, request, pk):
        if request.GET.get('from_session') == 'True':
            for service in get_services(request):
                if service.id == pk:
                    order_service = service
        else:
            order_service = get_object_or_404(OrderService, pk=pk)

        if order_service.service:
            service_id = order_service.service.id
        else:
            service_id = None

        return JsonResponse({
            'service': service_id,
            'name': order_service.name,
            'price_net': order_service.price_net,
            'quantity': order_service.quantity,
            'from_session': order_service.from_session,
        })


class OrderServiceUpdate(EmployeeRequiredMixin, UpdateView):
    model = OrderService
    form_class = OrderServiceForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        order_service_id = self.kwargs.get('pk')
        from_session = self.request.POST.get('from_session')

        if from_session == 'true':
            obj_temp = self.request.session[str(order_service_id)]
            if obj_temp['service']:
                service_instance = get_object_or_404(Service, pk=obj_temp['service'])
            else:
                service_instance = None
            obj_temp['service'] = service_instance
            obj_temp['from_session'] = 1
            obj = OrderService(**obj_temp)
        else:
            obj = super().get_object(queryset)

        return obj

    def form_valid(self, form):
        if self.object.from_session:
            self.request.session[str(self.object.id)] = model_to_dict(self.object)
            return JsonResponse({'status': 200})

        else:
            return super().form_valid(form)


class OrderServiceDelete(EmployeeRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_service_id = request.POST.get('pk')
        if request.POST.get('order_from_session') == 'True':
            if str(order_service_id) in [key for key in self.request.session.keys() if key.isdigit()]:
                self.request.session.pop(str(order_service_id), None)

                return JsonResponse({'status': 204})
            return JsonResponse({'status': 400})

        order_service = get_object_or_404(OrderService, pk=order_service_id)
        order_service.is_active = False
        order_service.save()

        return JsonResponse({'status': 204})


class SortNumberUpdateApiView(EmployeesOrdersList):
    object_list = ''

    def get_queryset(self, ):
        executor_id = self.request.POST.get('executor_id')
        queryset = super().get_queryset().filter(executor_id=executor_id).order_by('sort_number')

        return queryset

    def get_context_data(self, **kwargs):
        context = OrderListViewBase.get_context_data(self, **kwargs)

        return context

    def post(self, request, order_id, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        new_position = request.POST.get('new_position')
        table_id = request.POST.get('table_id')
        executor_id = request.POST.get('executor_id')

        sort_order_old = get_object_or_404(Order, pk=order_id)
        sort_order_new = get_object_or_404(Order, executor__id=executor_id, sort_number=new_position)

        sort_order_new.sort_number = sort_order_old.sort_number
        sort_order_old.sort_number = new_position

        sort_order_old.save()
        sort_order_new.save()

        orders = map_choices_int_to_str(self.get_queryset())

        context['orders'] = orders
        context['table_id'] = table_id

        return render(request, 'order_management/employees_order_management_list.html', context=context)


class GetReportApiView(EmployeeRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        executor = ThreadPoolExecutor()
        language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        employee = f'{self.request.user.first_name} {self.request.user.last_name}'
        future = executor.submit(get_report, order, employee, language)
        report_path = future.result()
        report_file_name = os.path.basename(report_path)

        response = FileResponse(open(report_path, 'rb'), content_type='application/pdf')

        response['Content-Disposition'] = f'attachment; filename={report_file_name}'

        return response


class SendReportApiView(EmployeeRequiredMixin, View):
    def get(self, request, order_id):
        language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        order = Order.objects.get(pk=order_id)
        email_to = request.GET.get('email_to')
        employee = f'{self.request.user.first_name} {self.request.user.last_name}'

        executor = ThreadPoolExecutor()
        future = executor.submit(get_report, order, employee, language)
        report_path = future.result()
        report_file_name = os.path.basename(report_path)

        email_body = settings.EMAIL_REPORT_BODY
        email_body = email_body.replace('#order_number', str(order.id))
        email_body = email_body.replace('#employee', employee)

        email = EmailMessage(
            settings.EMAIL_REPORT_TITLE,
            email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_to],
            reply_to=[settings.REPLY_TO],
        )
        with open(report_path, 'rb') as file:
            email.attach(report_file_name, file.read(), 'application/pdf')

        email.send()

        return JsonResponse({'status': 200})
