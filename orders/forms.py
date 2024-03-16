from dal import autocomplete
from django import forms

from .models import Order, AdditionalAddress
from customers.models import Customer
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

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super(OrderForm, self).__init__(*args, **kwargs)

        if self.instance.customer:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.filter(
                customer=self.instance.customer)
        else:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.none()

        if customer:
            self.fields['additional_address'].queryset = AdditionalAddress.objects.filter(customer=customer)

        for field in self.fields:
            if field == 'additional_info':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user_intake', 'approver']
