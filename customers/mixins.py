from abc import ABC

from django.shortcuts import get_object_or_404

from .models import Customer


class AddressContextMixin(ABC):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = get_object_or_404(Customer, pk=self.kwargs.get('customer_pk'))
        context['customer'] = customer
        return context
