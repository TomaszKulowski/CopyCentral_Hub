from json import loads

from dal import autocomplete
from django.db.models import Q
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from sorl.thumbnail import get_thumbnail


from .models import Attachment
from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from customers.models import Customer, AdditionalAddress
from devices.models import Device
from employees.models import Employee


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
        qs = AdditionalAddress.objects.filter(customer_id=customer_id, is_active=True)

        if self.q:
            qs = qs.filter(
                Q(city__icontains=self.q) |
                Q(street__icontains=self.q)
            )

        return qs


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

        return render(request, 'service_orders/attachments_list.html', {'attachments': attachments})
