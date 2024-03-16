from django import forms

from .models import ServiceOrder
from service_orders.models import Status


class ServiceOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceOrderForm, self).__init__(*args, **kwargs)

        if self.instance.order.executor:
            if self.instance.order.executor.department > 2:
                statuses = Status.choices.copy()
                del(statuses[3])
                self.fields['status'].choices = statuses
            else:
                self.fields['status'].choices = self.fields['status'].choices

        for field in self.fields:
            if field == 'name':
                self.fields[field].widget.attrs.update({'rows': 2})
            if field == 'description':
                self.fields[field].widget.attrs.update({'rows': 4})

            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = '__all__'
        model = ServiceOrder
        exclude = ['order', ]
