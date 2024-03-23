from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import UpdateView, CreateView, ListView

from .forms import ServiceForm, BrandForm, ModelForm
from .models import Service, Brand, Model
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class ServicesList(EmployeeRequiredMixin, View):
    def get(self, request):
        grouped_data = {}

        for service in Service.objects.select_related('device_brand', 'device_model').all():
            brand = service.device_brand
            model = service.device_model if service.device_model else "All"

            grouped_data.setdefault(brand, {})
            grouped_data[brand].setdefault(model, [])
            grouped_data[brand][model].append(service)

        for brand, models in grouped_data.items():
            all_services = models.pop('All', [])
            for services in models.values():
                services.extend(all_services)

        return render(request, 'services/services_list.html', {'grouped_data': grouped_data})


class ServiceDetails(EmployeeRequiredMixin, UpdateView):
    model = Service
    template_name = 'services/service_details.html'
    form_class = ServiceForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.disabled = True
        return form


class ServiceUpdate(EmployeeRequiredMixin, UpdateView):
    model = Service
    template_name = 'services/service_update.html'
    form_class = ServiceForm

    def get_success_url(self):
        return reverse_lazy('services:services_list')


class ServiceCreate(EmployeeRequiredMixin, CreateView):
    model = Service
    template_name = 'services/service_update.html'
    form_class = ServiceForm

    def get_success_url(self):
        return reverse_lazy('services:services_list')


class BrandsList(EmployeeRequiredMixin, ListView):
    model = Brand
    template_name = 'services/brands_list.html'


class BrandDetails(EmployeeRequiredMixin, UpdateView):
    model = Brand
    template_name = 'services/brand_details.html'
    form_class = BrandForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.disabled = True
        return form


class BrandUpdate(EmployeeRequiredMixin, UpdateView):
    model = Brand
    template_name = 'services/brand_update.html'
    form_class = BrandForm

    def get_success_url(self):
        return reverse_lazy('services:brands_list')


class BrandCreate(EmployeeRequiredMixin, CreateView):
    model = Brand
    template_name = 'services/brand_update.html'
    form_class = BrandForm

    def get_success_url(self):
        return reverse_lazy('services:brands_list')


class ModelsList(EmployeeRequiredMixin, ListView):
    model = Model
    template_name = 'services/models_list.html'


class ModelDetails(EmployeeRequiredMixin, UpdateView):
    model = Model
    template_name = 'services/model_details.html'
    form_class = ModelForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.disabled = True
        return form


class ModelUpdate(EmployeeRequiredMixin, UpdateView):
    model = Model
    template_name = 'services/model_update.html'
    form_class = ModelForm

    def get_success_url(self):
        return reverse_lazy('services:models_list')


class ModelCreate(EmployeeRequiredMixin, CreateView):
    model = Model
    template_name = 'services/model_update.html'
    form_class = ModelForm

    def get_success_url(self):
        return reverse_lazy('services:models_list')
