from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords


class Payment(models.IntegerChoices):
    CASH = 0, _('Cash')
    BANK = 1, _('Bank')


class Customer(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='customer',
        blank=True,
        null=True,
        verbose_name=_('User'),
    )
    name = models.TextField(_('Full Name or Company Name'), max_length=255)
    tax = models.CharField(_('Tax'), max_length=15, blank=True, null=True)
    billing_country = models.CharField(_('Billing Country'), max_length=24, blank=True, null=True)
    billing_city = models.CharField(_('Billing City'), max_length=24, blank=True, null=True)
    billing_postal_code = models.CharField(_('Billing Postal Code'), max_length=24, blank=True, null=True)
    billing_street = models.CharField(_('Billing Street'), max_length=60, blank=True, null=True)
    billing_number = models.CharField(_('Billing Number'), max_length=24, blank=True, null=True)
    country_calling_code = models.CharField(_('Calling Code'), max_length=8, blank=True, null=True)
    phone_number = models.BigIntegerField(_('Phone Number'), blank=True, null=True)
    email = models.EmailField(_('Email'), blank=True, null=True)
    description = models.TextField(_('Description'), max_length=300, blank=True, null=True)
    payment = models.SmallIntegerField(_('Payment'), choices=Payment.choices, default=Payment.CASH)
    history = HistoricalRecords()

    def __str__(self):
        if self.name and self.tax:
            return f'{self.name}; ' + _('Tax') + f': {self.tax}'
        return self.name

    def get_address(self):
        address = ''
        fields = [self.billing_city, self.billing_postal_code, self.billing_street, self.billing_number]
        for field in fields:
            if field:
                if field == self.billing_city:
                    address += self.billing_city
                    address += ' - '
                elif field == self.billing_postal_code:
                    address += self.billing_postal_code
                    address += ', '
                elif field == self.billing_street:
                    address += self.billing_street
                    address += ' '
                elif field == self.billing_number:
                    address += self.billing_number
        return address


class AdditionalAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_('Customer'))
    country = models.CharField(_('Country'), max_length=24, blank=True, null=True)
    city = models.CharField(_('City'), max_length=24)
    postal_code = models.CharField(_('Postal Code'), max_length=24, blank=True, null=True)
    street = models.CharField(_('Street'), max_length=24, blank=True, null=True)
    number = models.CharField(_('Number'), max_length=24, blank=True, null=True)
    description = models.TextField(_('Description'), max_length=200, blank=True, null=True)
    is_active = models.BooleanField(_('Is Active'), default=True)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        address = ''
        fields = [self.city, self.postal_code, self.street, self.number]
        for field in fields:
            if field:
                if field == self.city:
                    address += self.city
                elif field == self.postal_code:
                    address += ' - '
                    address += self.postal_code
                elif field == self.street:
                    address += ', '
                    address += self.street
                elif field == self.number:
                    address += ' '
                    address += self.number
        return address
