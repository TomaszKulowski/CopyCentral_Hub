from django import forms

from .models import Service, Brand, Model


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            if field_name == 'description':
                self.fields[field_name].widget.attrs.update({'rows': 4})

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = Service


class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = Brand


class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f'* {field.label}'

            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = Model
