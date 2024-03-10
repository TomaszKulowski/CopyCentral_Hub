from django import forms

from .models import ServiceOrder


class ServiceOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'name':
                self.fields[field].widget.attrs.update({'rows': 2})
            if field == 'description':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = ServiceOrder
