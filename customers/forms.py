from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Customer, AdditionalAddress


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            if field_name == 'name':
                self.fields[field_name].widget.attrs.update({'rows': 2})
            if field_name == 'description':
                self.fields[field_name].widget.attrs.update({'rows': 4})

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        exclude = ('user', )
        model = Customer


class AdditionalAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdditionalAddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            if field_name == 'customer':
                self.fields[field_name].widget = forms.HiddenInput()
            if field_name == 'description':
                self.fields[field_name].widget.attrs.update({'rows': 4})

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = AdditionalAddress
        widgets = {
            'is_active': forms.Select(choices=[(True, _('Yes')), (False, _('No'))])
        }
