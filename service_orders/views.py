from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import ServiceOrderForm
from .models import ServiceOrder
from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from customers.forms import Customer, CustomerForm, AdditionalAddressForm
from customers.models import AdditionalAddress
from orders.forms import OrderForm


class ServiceOrderList(EmployeeRequiredMixin, ListView):
    model = ServiceOrder
    template_name = 'service_orders/service_orders_list.html'
    paginate_by = 10

    def get_template_names(self):
        search_query = self.request.GET.get('search', False)
        if search_query or search_query == '':
            return ['service_orders/service_orders_list_table.html']
        return super().get_template_names()

    def get_queryset(self):
        service_orders = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            service_orders = service_orders.filter(
                Q(id__contains=search_query) |
                Q(order__customer__name__icontains=search_query) |
                Q(order__invoice_number__icontains=search_query) |
                Q(order__device__serial_number__icontains=search_query)
            )
        return service_orders


class ServiceOrderDetails(EmployeeRequiredMixin, UpdateView):
    model = ServiceOrder
    template_name = 'service_orders/service_order_details.html'
    form_class = ServiceOrderForm
    order_form_class = OrderForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_form = self.order_form_class(instance=self.object.order)
        for field_name, field in order_form.fields.items():
            field.disabled = True
            if field_name == 'additional_info':
                field.widget.attrs.update({'rows': 4})

        context['order_form'] = order_form
        context['object'] = self.object
        return context


class ServiceOrderUpdate(EmployeeRequiredMixin, View):
    model = ServiceOrder
    template_name = 'service_orders/service_order_update.html'
    service_order_form_class = ServiceOrderForm
    order_form_class = OrderForm
    customer_form_class = CustomerForm
    address_form_class = AdditionalAddressForm

    def get_context_data(self, **kwargs):
        customer_id = kwargs.get('customer_id')
        payer_id = kwargs.get('payer_id')
        address_id = kwargs.get('address_id')

        service_order_instance = get_object_or_404(self.model.objects.select_related(), pk=kwargs.get('pk'))
        if customer_id:
            customer_instance = get_object_or_404(Customer, pk=customer_id)
            service_order_instance.order.customer = customer_instance
        if payer_id:
            payer_instance = get_object_or_404(Customer, pk=payer_id)
            service_order_instance.order.payer = payer_instance
        if address_id == 'null':
            service_order_instance.order.additional_address = None
        elif address_id:
            address_instance = get_object_or_404(AdditionalAddress, pk=address_id)
            service_order_instance.order.additional_address = address_instance

        service_order_form = self.service_order_form_class(instance=service_order_instance)
        order_form = self.order_form_class(instance=service_order_instance.order)

        context = {
            'service_order_instance': service_order_instance,
            'service_order_form': service_order_form,
            'order_form': order_form,
            'customer_form': self.customer_form_class(),
            'address_form': self.address_form_class(),
        }
        return context

    def post(self, request, *args, **kwargs):
        service_order_instance = get_object_or_404(self.model.objects.select_related(), pk=kwargs.get('pk'))
        service_order_form = self.service_order_form_class(request.POST, instance=service_order_instance)

        request_data = request.POST.copy()
        address_id = request_data.pop('additional_address', None)
        if address_id:
            address_id = address_id.pop()

        order_form = self.order_form_class(request_data, instance=service_order_instance.order)

        if service_order_form.is_valid() and order_form.is_valid():
            service_order_form.save()
            if address_id:
                order_instance = order_form.save(commit=False)
                address_instance = get_object_or_404(AdditionalAddress, pk=address_id)
                customer_id = request_data.get('customer')
                customer_instance = get_object_or_404(Customer, pk=customer_id)
                if address_instance in customer_instance.additionaladdress_set.all():
                    order_instance.additional_address = address_instance
                    order_instance.save()
                else:
                    context = self.get_context_data(**kwargs)
                    context['form'] = service_order_form
                    context['order_form'] = order_form
                    return render(request, self.template_name, context)
            else:
                order_form.save()
            return HttpResponseRedirect(reverse_lazy('service_orders:details', kwargs={'pk': kwargs.get('pk')}))

        else:
            context = self.get_context_data(**kwargs)
            context['form'] = service_order_form
            context['order_form'] = order_form
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
            )
        )


class ServiceOrderCreate(EmployeeRequiredMixin, CreateView):
    model = ServiceOrder
    template_name = 'service_orders/service_order_update.html'
    form_class = ServiceOrderForm

    def get_success_url(self):
        return reverse_lazy('service_orders:service_order_details', kwargs={'pk': self.object.pk})


class CustomerDetails(EmployeeRequiredMixin, DetailView):
    model = Customer
    template_name = 'service_orders/customer_details.html'


class CustomerCreateModal(EmployeeRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm

    def form_valid(self, form):
        customer_instance = form.save()
        customer_id = customer_instance.id
        return JsonResponse({'success': True, 'customer_id': customer_id})


class AddressDetails(EmployeeRequiredMixin, DetailView):
    model = AdditionalAddress
    template_name = 'service_orders/address_details.html'


class AddressCreateModal(EmployeeRequiredMixin, CreateView):
    model = AdditionalAddress
    form_class = AdditionalAddressForm

    def form_valid(self, form):
        address_instance = form.save()
        address_id = address_instance.id
        return JsonResponse({'success': True, 'address_id': address_id})
