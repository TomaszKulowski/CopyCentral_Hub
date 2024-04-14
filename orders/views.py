import os

from concurrent.futures import ThreadPoolExecutor
from json import loads

from dal import autocomplete
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Q
from django.forms import ModelForm
from django.http import FileResponse, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from sorl.thumbnail import get_thumbnail

from .forms import OrderForm, OrderServicesForm, AttachmentForm, AttachmentFormSet
from .models import Attachment, Order, Region, PriorityChoices, OrderServices
from .utils import get_report
from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from customers.forms import CustomerForm, AdditionalAddressForm
from customers.models import Customer, AdditionalAddress
from devices.forms import DeviceForm
from devices.models import Device
from employees.models import Employee
from order_management.views import EmployeesOrdersList, OrderListViewBase
from orders.utils import map_choices_int_to_str
from services.models import Brand, Model, Service


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
                Q(telephone__icontains=self.q)
            )

        return qs


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

        return qs


class AddressAutocomplete(EmployeeRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return AdditionalAddress.objects.none()

        customer_id = loads(self.request.GET.get('forward')).get('customer')
        if customer_id:
            qs = AdditionalAddress.objects.filter(customer_id=customer_id, is_active=True)

            if self.q:
                qs = qs.filter(
                    Q(city__icontains=self.q) |
                    Q(street__icontains=self.q)
                )

            return qs
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

        return qs


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

        return JsonResponse({'success': 'true'})


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
        context['order_by'] = order_by
        context['page_objs'] = context['page_obj']
        del context['page_obj']

        return context


class OrderUpdate(EmployeeRequiredMixin, View):
    model = Order
    template_name = 'orders/order_update.html'
    order_form_class = OrderForm
    customer_form_class = CustomerForm
    address_form_class = AdditionalAddressForm
    device_form_class = DeviceForm
    service_form_class = OrderServicesForm
    attachment_formset = AttachmentFormSet

    def get_context_data(self, **kwargs):
        order_id = kwargs.get('pk')
        customer_id = kwargs.get('customer_id')
        payer_id = kwargs.get('payer_id')
        address_id = kwargs.get('address_id')
        device_id = kwargs.get('device_id')

        if order_id:
            order_instance = get_object_or_404(self.model.objects.select_related(), pk=order_id)
        else:
            order_instance = self.model.objects.create(user_intake=self.request.user.employee.first())

        if customer_id:
            customer_instance = get_object_or_404(Customer, pk=customer_id)
            order_instance.customer = customer_instance
            if not order_instance.contact:
                order_instance.contact = customer_instance.telephone
        if payer_id:
            payer_instance = get_object_or_404(Customer, pk=payer_id)
            order_instance.payer = payer_instance
        if address_id == 'null':
            order_instance.additional_address = None
        if address_id:
            address_instance = get_object_or_404(AdditionalAddress, pk=address_id)
            order_instance.additional_address = address_instance
        if device_id:
            device_instance = get_object_or_404(Device, pk=device_id)
            order_instance.device = device_instance

        atts = order_instance.attachment_set.all()
        attachments = {}
        for att in atts:
            if att.image:
                attachments[att.id] = {'image': get_thumbnail(att.image.name, '300x300', crop='center', quality=20)}
            else:
                attachments[att.id] = {'filename': os.path.basename(att.file.name)}

        order_form = self.order_form_class(instance=order_instance)

        order_services = order_instance.services.all()
        total_summary = sum(service.quantity * service.price_net for service in order_services)

        context = {
            'order_instance': order_instance,
            'order_form': order_form,
            'customer_form': self.customer_form_class(),
            'address_form': self.address_form_class(),
            'device_form': self.device_form_class(),
            'service_form': self.service_form_class(),
            'attachment_formset': self.attachment_formset(queryset=Attachment.objects.none()),
            'attachments': attachments,
            'total_summary': total_summary,
            'brands': Brand.objects.all(),
            'models': Model.objects.all(),
        }

        return context

    def post(self, request, *args, **kwargs):
        add_service = request.POST.get('add_service')

        order_instance = get_object_or_404(self.model.objects.select_related(), pk=kwargs.get('pk'))

        if not order_instance.contact and order_instance.customer:
            order_instance.contact = order_instance.customer.telephone

        if add_service:
            service_instance = get_object_or_404(Service, pk=request.POST.get('service'))
            order_service_id = request.POST.get('order_service_id')

            if order_service_id:
                order_service_instance = get_object_or_404(OrderServices, pk=order_service_id)
                order_service_instance.service = service_instance
                order_service_instance.name = request.POST.get('name')
                order_service_instance.price_net = request.POST.get('price_net')
                order_service_instance.quantity = request.POST.get('quantity')
                order_service_instance.save()
            else:
                order_service_instance = OrderServices.objects.create(
                    service=service_instance,
                    name=request.POST.get('name'),
                    price_net=request.POST.get('price_net'),
                    quantity=request.POST.get('quantity'),
                )
                order_instance.services.add(order_service_instance),0

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
                customer_instance = get_object_or_404(Customer, pk=customer_id)
                if address_instance in customer_instance.additionaladdress_set.all():
                    order_instance.additional_address = address_instance
                else:
                    context = self.get_context_data(**kwargs)

                    return render(request, self.template_name, context)

            order_instance.save()

            return HttpResponseRedirect(reverse_lazy('orders:order_details', kwargs={'pk': kwargs.get('pk')}))

        else:
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
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


class CustomerDetails(EmployeeRequiredMixin, DetailView):
    model = Customer
    template_name = 'orders/customer_details.html'


class CustomerCreateModal(EmployeeRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm

    def form_valid(self, form):
        customer_instance = form.save()
        customer_id = customer_instance.id

        return JsonResponse({'success': True, 'customer_id': customer_id})


class AddressDetails(EmployeeRequiredMixin, DetailView):
    model = AdditionalAddress
    template_name = 'orders/address_details.html'


class AddressCreateModal(EmployeeRequiredMixin, CreateView):
    model = AdditionalAddress
    form_class = AdditionalAddressForm

    def form_valid(self, form):
        address_instance = form.save()
        address_id = address_instance.id

        return JsonResponse({'success': True, 'address_id': address_id})


class DeviceCreateModal(EmployeeRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm

    def form_valid(self, form):
        device_instance = form.save()
        device_id = device_instance.id

        return JsonResponse({'success': True, 'device_id': device_id})


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


class ServicesList(EmployeeRequiredMixin, ListView):
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        services = order.services.all()

        services_data = []
        for service in services:
            service_data = {
                'id': service.id,
                'name': service.name.title(),
                'price_net': service.price_net,
                'quantity': service.quantity,
            }
            services_data.append(service_data)

        return JsonResponse({'services': services_data})


class ServiceUpdate(EmployeeRequiredMixin, UpdateView):
    model = OrderServices
    fields = ['service', 'name', 'price_net', 'quantity']

    def get_object(self, queryset=None):
        service_id = self.request.GET.get('service_id')
        if service_id and service_id != 'undefined':
            return get_object_or_404(OrderServices, pk=service_id)
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        context_dict = {
            'id': context['object'].id,
            'service': context['object'].service.id,
            'name': context['object'].name,
            'price_net': context['object'].price_net,
            'quantity': context['object'].quantity,
        }

        return JsonResponse(context_dict)


class ServiceDelete(EmployeeRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        service = get_object_or_404(OrderServices, pk=request.POST.get('pk'))
        order = Order.objects.filter(services=service)
        if order:
            order[0].services.remove(service)

        return JsonResponse({'success': True})


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
