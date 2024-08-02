from django import forms

from .models import Device


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            if field_name == 'description':
                self.fields[field_name].widget.attrs.update({'rows': 4})

            if field_name == 'total_counter':
                self.fields[field_name].widget.attrs.update({'id': 'total_counter_device', 'readonly': 'True'})
            if field_name == 'mono_counter':
                self.fields[field_name].widget.attrs.update({'id': 'mono_counter_device'})
            if field_name == 'color_counter':
                self.fields[field_name].widget.attrs.update({'id': 'color_counter_device'})

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Device
        fields = '__all__'
