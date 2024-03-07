from django import forms

from .models import Device


class DeviceUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'description':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Device
        fields = '__all__'
