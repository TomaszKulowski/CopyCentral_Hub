from django import forms

from .models import Contractor


class ContractorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContractorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        exclude = ('user', 'transfer_payment', )
        model = Contractor
