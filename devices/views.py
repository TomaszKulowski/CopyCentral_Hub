from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from .forms import DeviceForm
from .models import Device
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class DevicesList(EmployeeRequiredMixin, ListView):
    model = Device
    template_name = 'devices/list.html'
    paginate_by = 10

    def get_template_names(self):
        search_query = self.request.GET.get('search', False)
        if search_query or search_query == '':
            return ['devices/list_table.html']
        return super().get_template_names()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(serial_number__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeviceDetails(EmployeeRequiredMixin, UpdateView):
    model = Device
    template_name = 'devices/details.html'
    form_class = DeviceForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.disabled = True
        return form


class DeviceUpdate(EmployeeRequiredMixin, UpdateView):
    model = Device
    template_name = 'devices/update.html'
    form_class = DeviceForm

    def get_success_url(self):
        return reverse_lazy('devices:details', kwargs={'pk': self.object.pk})


class DeviceCreate(EmployeeRequiredMixin, CreateView):
    model = Device
    template_name = 'devices/update.html'
    form_class = DeviceForm

    def get_success_url(self):
        return reverse_lazy('devices:details', kwargs={'pk': self.object.pk})
