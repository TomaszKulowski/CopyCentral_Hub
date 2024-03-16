from django.contrib.auth import get_user_model
from django.db import models


class Payment(models.IntegerChoices):
    CASH = 0, 'Cash'
    BANK = 1, 'Bank'


class Customer(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='customer',
        blank=True,
        null=True,
    )
    name = models.TextField(max_length=255, help_text='Full Name or Company Name')
    tax = models.CharField(max_length=15, blank=True, null=True)
    billing_country = models.CharField(max_length=24, blank=True, null=True)
    billing_city = models.CharField(max_length=24, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=24, blank=True, null=True)
    billing_street = models.CharField(max_length=24, blank=True, null=True)
    billing_number = models.CharField(max_length=24, blank=True, null=True)
    country_calling_code = models.CharField(max_length=8, blank=True, null=True, help_text='Calling Code')
    telephone = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    transfer_payment = models.SmallIntegerField(choices=Payment.choices, default=Payment.CASH)

    def __str__(self):
        return f'{self.name}; Tax: {self.tax}'


class AdditionalAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    country = models.CharField(max_length=24, blank=True, null=True)
    city = models.CharField(max_length=24)
    postal_code = models.CharField(max_length=24, blank=True, null=True)
    street = models.CharField(max_length=24, blank=True, null=True)
    number = models.CharField(max_length=24, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.city}, {self.street} {self.number}'
