from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import ListView, UpdateView, CreateView

from .forms import ServiceOrderForm
from .models import ServiceOrder
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for key, value in form.fields.items():
            value.disabled = True
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_order = get_object_or_404(ServiceOrder.objects.select_related(), pk=self.kwargs.get('pk'))

        address = {}
        if service_order.additional_address:
            address['city'] = service_order.additional_address.city
            address['street'] = service_order.additional_address.street
            address['number'] = service_order.additional_address.number
        else:
            address['city'] = service_order.order.customer.billing_city
            address['street'] = service_order.order.customer.billing_street
            address['number'] = service_order.order.customer.billing_number

        context['address'] = address
        context['customer_info'] = service_order.order.customer
        context['service_order'] = service_order
        return context


class ServiceOrderUpdate(EmployeeRequiredMixin, UpdateView):
    model = ServiceOrder
    template_name = 'service_orders/update.html'
    form_class = ServiceOrderForm

    def get_success_url(self):
        return reverse_lazy('service_orders:details', kwargs={'pk': self.object.pk})


class ServiceOrderCreate(EmployeeRequiredMixin, CreateView):
    model = ServiceOrder
    template_name = 'service_orders/update.html'
    form_class = ServiceOrderForm

    def get_success_url(self):
        return reverse_lazy('service_orders:details', kwargs={'pk': self.object.pk})
