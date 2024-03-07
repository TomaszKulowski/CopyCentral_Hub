from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'description':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = Service
