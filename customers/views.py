from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView

from .forms import CustomerForm, AdditionalAddressForm
from .mixins import AddressContextMixin
from .models import Customer, AdditionalAddress
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class CustomerList(EmployeeRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all()
        search_query = request.GET.get('search', False)

        if search_query:
            customers = customers.filter(
                Q(name__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(tax__icontains=search_query) |
                Q(billing_city__icontains=search_query) |
                Q(billing_street__icontains=search_query) |
                Q(telephone__icontains=search_query)
            )

        page = request.GET.get('page')
        paginator = Paginator(customers, 10)
        page_obj = paginator.get_page(page)

        if search_query or search_query == '':
            return render(request, 'customers/customers_list_table.html', {'page_obj': page_obj})

        return render(request, 'customers/customers_list.html', {'page_obj': page_obj})


class CustomerDetails(EmployeeRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/customer_details.html'
    form_class = CustomerForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        forms = {}
        for key, value in form.fields.items():
            value.disabled = True
            forms[key] = value
        return form


class CustomerUpdate(EmployeeRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/customer_update.html'
    form_class = CustomerForm

    def get_success_url(self):
        return reverse_lazy('customers:customer_details', kwargs={'pk': self.object.pk})


class CustomerCreate(EmployeeRequiredMixin, CreateView):
    model = Customer
    template_name = 'customers/customer_update.html'
    form_class = CustomerForm

    def get_success_url(self):
        return reverse_lazy('customers:customer_details', kwargs={'pk': self.object.pk})


class AdditionalAddressesList(AddressContextMixin, EmployeeRequiredMixin, ListView):
    model = AdditionalAddress
    template_name = 'customers/addresses_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        customer_pk = self.kwargs.get('customer_pk')
        queryset = AdditionalAddress.objects.filter(customer_id=customer_pk, is_active=True)
        return queryset


class AdditionalAddressDetails(AddressContextMixin, EmployeeRequiredMixin, UpdateView):
    model = AdditionalAddress
    template_name = 'customers/address_details.html'
    form_class = AdditionalAddressForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for key, value in form.fields.items():
            value.disabled = True
        return form


class AdditionalAddressUpdate(AddressContextMixin, EmployeeRequiredMixin, UpdateView):
    model = AdditionalAddress
    template_name = 'customers/address_update.html'
    form_class = AdditionalAddressForm

    def get_success_url(self):
        return reverse_lazy('customers:addresses_list', kwargs={'customer_pk': self.kwargs.get('customer_pk')})

    def post(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs.get('customer_pk'))
        data = request.POST.copy()
        data['customer'] = customer
        address_instance = self.get_object()
        address_form = AdditionalAddressForm(data, instance=address_instance)

        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseBadRequest()


class AdditionalAddressCreate(AddressContextMixin, EmployeeRequiredMixin, CreateView):
    model = AdditionalAddress
    template_name = 'customers/address_update.html'
    form_class = AdditionalAddressForm

    def get_success_url(self):
        return reverse_lazy('customers:customer_details', kwargs={'pk': self.kwargs.get('customer_pk')})

    def post(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs.get('customer_pk'))
        data = request.POST.copy()
        data['customer'] = customer
        address_form = AdditionalAddressForm(data)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseBadRequest()


class AdditionalAddressDelete(DeleteView):
    model = AdditionalAddress
    success_url = reverse_lazy('success_url')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
