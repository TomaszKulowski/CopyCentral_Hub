from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from .forms import ServiceOrderForm
from .models import ServiceOrder
from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from customers.forms import Customer, CustomerForm, AdditionalAddressForm
from customers.models import AdditionalAddress
from orders.forms import OrderForm
from services.forms import ServiceForm


class ServiceOrderList(EmployeeRequiredMixin, ListView):
    model = ServiceOrder
    template_name = 'service_orders/list.html'
    paginate_by = 10

    def get_template_names(self):
        search_query = self.request.GET.get('search', False)
        if search_query or search_query == '':
            return ['service_orders/list_table.html']
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
    template_name = 'service_orders/details.html'
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
    template_name = 'service_orders/update.html'
    service_order_form_class = ServiceOrderForm
    order_form_class = OrderForm
    customer_form_class = CustomerForm
    address_form_class = AdditionalAddressForm

    def get_context_data(self, **kwargs):
        service_order_instance = get_object_or_404(self.model.objects.select_related(), pk=kwargs.get('pk'))

        service_order_form = self.service_order_form_class(instance=service_order_instance)
        order_form = self.order_form_class(instance=service_order_instance.order)

        context = {
            'service_order_instance': service_order_instance,
            'service_order_form': service_order_form,
            'order_form': order_form,
        }
        return context

    def post(self, request, *args, **kwargs):
        service_order_instance = get_object_or_404(self.model.objects.select_related(), pk=kwargs.get('pk'))

        service_order_form = self.service_order_form_class(request.POST, instance=service_order_instance)

        request_data = request.POST.copy()
        address_id = request_data.pop('additional_address').pop()

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
        return render(request, self.template_name, context=self.get_context_data(pk=kwargs.get('pk')))


class ServiceOrderCreate(EmployeeRequiredMixin, CreateView):
    model = ServiceOrder
    template_name = 'service_orders/update.html'
    form_class = ServiceOrderForm

    def get_success_url(self):
        return reverse_lazy('service_orders:details', kwargs={'pk': self.object.pk})


class CustomerDetails(EmployeeRequiredMixin, DetailView):
    model = Customer
    template_name = 'service_orders/customer_details.html'


class AddressDetails(EmployeeRequiredMixin, DetailView):
    model = AdditionalAddress
    template_name = 'service_orders/address_details.html'
