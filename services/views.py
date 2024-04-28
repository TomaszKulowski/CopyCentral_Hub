from collections import OrderedDict

from django.db.models import Q
from django.urls import reverse_lazy

from django.views.generic import UpdateView, CreateView, ListView

from .forms import ServiceForm, BrandForm, ModelForm
from .models import Service, Brand, Model
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class ServicesList(EmployeeRequiredMixin, ListView):
    model = Service
    template_name = 'services/services_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        active_brands = Brand.objects.filter(is_active=True)
        active_models = Model.objects.filter(is_active=True)
        queryset = Service.objects.select_related('device_brand', 'device_model')
        queryset = queryset.filter(
            Q(device_model__in=active_models, device_brand__in=active_brands) |
            Q(device_model=None, device_brand__in=active_brands) |
            Q(device_model__in=active_models, device_brand=None) |
            Q(device_model=None, device_brand=None),
            is_active=True
        )
        queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped_data = {}

        for service in context['services']:
            brand = service.device_brand
            model = service.device_model if service.device_model else "All"

            grouped_data.setdefault(brand, {})
            grouped_data[brand].setdefault(model, [])
            grouped_data[brand][model].append(service)

        for brand, models in grouped_data.items():
            if brand.name == 'Basic Services':
                continue
            all_services = models.pop('All', [])
            for services in models.values():
                services.extend(all_services)

        sorted_grouped_data = OrderedDict(
            sorted(grouped_data.items(), key=lambda item: (item[0].name != 'Basic Services', item[0].name.casefold()))
        )
        for brand, models in sorted_grouped_data.items():
            sorted_models = OrderedDict(
                sorted(models.items(), key=lambda item: item[0].name.casefold() if item[0] != "All" else "")
            )
            sorted_grouped_data[brand] = sorted_models

        context['grouped_data'] = sorted_grouped_data

        return context


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
