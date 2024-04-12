from dal import autocomplete
from django import forms

from .models import Order, AdditionalAddress, Attachment, StatusChoices, OrderServices
from customers.models import Customer
from devices.models import Device
from employees.models import Employee


class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        label='Customer',
        widget=autocomplete.ModelSelect2(
            forward=('customer', ),
            url='orders:customer_autocomplete',
            attrs={
                'data-placeholder': 'Customer ...',
                'data-ajax--delay': '500',
                'style': 'width:90%',
            }
        )
    )
    additional_address = forms.ModelChoiceField(
        required=False,
        queryset=AdditionalAddress.objects.all(),
        label='Additional Address',
        widget=autocomplete.ModelSelect2(
            forward=('customer',),
            url='orders:address_autocomplete',
            attrs={
                'data-placeholder': 'Service Address ... If empty, use billing address',
                'data-ajax--delay': '500',
                'style': 'width:90%',
            }
        )
    )
    payer = forms.ModelChoiceField(
        required=False,
        queryset=Customer.objects.all(),
        label='Payer',
        widget=autocomplete.ModelSelect2(
            forward=('payer', ),
            url='orders:customer_autocomplete',
            attrs={
                'data-placeholder': 'Payer ...',
                'data-ajax--delay': '500',
                'style': 'width:90%',
            }
        )
    )
    executor = forms.ModelChoiceField(
        required=False,
        queryset=Employee.objects.all(),
        label='Executor',
        widget=autocomplete.ModelSelect2(
            forward=('executor', ),
            url='orders:executor_autocomplete',
            attrs={
                'data-placeholder': 'Executor ...',
                'data-ajax--delay': '500',
                'style': 'width:100%',
            }
        )
    )
    device = forms.ModelChoiceField(
        required=False,
        queryset=Device.objects.all(),
        label='Device',
        widget=autocomplete.ModelSelect2(
            url='orders:device_autocomplete',
            attrs={
                'data-placeholder': 'Device ...',
                'data-ajax--delay': '500',
                'style': 'width:90%',
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
                customer=self.instance.customer)
        else:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.none()

        if customer:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.filter(customer=customer)

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


class OrderServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderServicesForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'service':
                self.fields[field].widget.attrs.update({'id': 'id_service_services'})
            if field == 'name':
                self.fields[field].widget.attrs.update({'id': 'id_service_name'})
            if field == 'price_net':
                self.fields[field].widget.attrs.update({'id': 'id_service_price_net'})
            if field == 'quantity':
                self.fields[field].widget.attrs.update({'id': 'id_service_quantity'})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = OrderServices
        fields = '__all__'


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
