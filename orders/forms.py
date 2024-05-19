from dal import autocomplete
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order, AdditionalAddress, Attachment, StatusChoices, OrderService
from customers.models import Customer
from devices.models import Device
from employees.models import Employee
from services.models import Service


class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label=_('Customer'),
        widget=autocomplete.ModelSelect2(
            forward=('customer', ),
            url='orders:customer_autocomplete_api',
            attrs={
                'data-placeholder': _('Customer ...'),
                'data-ajax--delay': '500',
                'style': 'width:90%',
                'id': 'customer-select'
            }
        )
    )
    additional_address = forms.ModelChoiceField(
        required=False,
        queryset=AdditionalAddress.objects.all(),
        label=_('Additional Address'),
        widget=autocomplete.ModelSelect2(
            url='orders:address_autocomplete_api',
            attrs={
                'data-placeholder': _('Service Address ... If empty, use billing address'),
                'data-ajax--delay': '500',
                'style': 'width:90%',
                'id': 'additional_address-select'
            }
        )
    )
    payer = forms.ModelChoiceField(
        required=False,
        queryset=Customer.objects.all(),
        label=_('Payer'),
        widget=autocomplete.ModelSelect2(
            forward=('payer', ),
            url='orders:customer_autocomplete_api',
            attrs={
                'data-placeholder': _('Payer ...'),
                'data-ajax--delay': '500',
                'style': 'width:90%',
                'id': 'payer-select',
            }
        )
    )
    executor = forms.ModelChoiceField(
        required=False,
        queryset=Employee.objects.all(),
        label=_('Executor'),
        widget=autocomplete.ModelSelect2(
            forward=('executor', ),
            url='orders:executor_autocomplete_api',
            attrs={
                'data-placeholder': _('Executor ...'),
                'data-ajax--delay': '500',
                'style': 'width:100%',
            }
        )
    )
    device = forms.ModelChoiceField(
        required=False,
        queryset=Device.objects.all(),
        label=_('Device'),
        widget=autocomplete.ModelSelect2(
            url='orders:device_autocomplete_api',
            attrs={
                'data-placeholder': _('Device ...'),
                'data-ajax--delay': '500',
                'style': 'width:90%',
                'id': 'device-select',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        if self.instance.executor:
            if self.instance.executor.department > 2:
                statuses = StatusChoices.choices.copy()
                del(statuses[3])
                self.fields['status'].choices = statuses
            else:
                self.fields['status'].choices = self.fields['status'].choices

        if self.instance.customer:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.filter(
                customer=self.instance.customer,
                is_active=True,
            )

        if customer:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.filter(
                customer=customer,
                is_active=True,
            )

        for field in self.fields:
            if field == 'name':
                self.fields[field].widget.attrs.update({'rows': 2})
            if field in ['additional_info', 'description']:
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user_intake', 'approver']


class OrderServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        required=False,
        queryset=Service.objects.all(),
        label=_('Service'),
        widget=autocomplete.ModelSelect2(
            url='orders:service_autocomplete_api',
            attrs={
                'data-placeholder': _('Service ...'),
                'data-ajax--delay': '500',
                'style': 'width:100%',
                'id': 'id_service_services',
                "data-dropdown-parent": "#addServiceModal",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(OrderServiceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            if field_name == 'name':
                self.fields[field_name].widget.attrs.update({'id': 'id_service_name'})
            if field_name == 'price_net':
                self.fields[field_name].widget.attrs.update({'id': 'id_service_price_net'})
            if field_name == 'quantity':
                self.fields[field_name].widget.attrs.update({'id': 'id_service_quantity'})
            if field_name == 'from_session':
                self.fields[field_name].widget = forms.HiddenInput()
                self.fields[field_name].widget.attrs.update({'id': 'id_service_from_session'})

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = OrderService
        fields = '__all__'
        exclude = ['is_active']


class AttachmentForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/png, image/jpeg', 'onchange': 'checkFileSize(this)'})
    )
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'application/pdf', 'onchange': 'checkFileSize(this)'})
    )

    class Meta:
        model = Attachment
        fields = ['image', 'file']


AttachmentFormSet = forms.modelformset_factory(Attachment, form=AttachmentForm)
