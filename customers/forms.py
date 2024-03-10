from django import forms

from .models import Customer, AdditionalAddress


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'name':
                self.fields[field].widget.attrs.update({'rows': 2})
            if field == 'description':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        exclude = ('user', )
        model = Customer


class AdditionalAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdditionalAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = AdditionalAddress
        widgets = {
            'is_active': forms.Select(choices=[(True, 'Yes'), (False, 'No')])
        }
