from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView

from .forms import DeviceUpdateForm
from .models import Device


class DevicesList(LoginRequiredMixin, View):
    def get(self, request):
        devices = Device.objects.all()
        search_query = request.GET.get('search', False)

        if search_query:
            devices = devices.filter(
                Q(serial_number__icontains=search_query)
            )

        page = request.GET.get('page')
        paginator = Paginator(devices, 10)
        page_obj = paginator.get_page(page)

        if search_query or search_query == '':
            return render(request, 'devices/list_table.html', {'page_obj': page_obj})

        return render(request, 'devices/list.html', {'page_obj': page_obj})


class DeviceDetails(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = 'devices/details.html'
    form_class = DeviceUpdateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        forms = {}
        for key, value in form.fields.items():
            value.disabled = True
            forms[key] = value
        return form


class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'devices/update.html'
    form_class = DeviceUpdateForm

    def get_success_url(self):
        return reverse_lazy('devices:details', kwargs={'pk': self.object.pk})


class DeviceCreate(CreateView):
    model = Device
    template_name = 'devices/update.html'
    form_class = DeviceUpdateForm

    def get_success_url(self):
        return reverse_lazy('devices:details', kwargs={'pk': self.object.pk})
