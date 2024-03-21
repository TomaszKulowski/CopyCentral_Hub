from django.db import models
from jsignature.fields import JSignatureField

from customers.models import Customer, AdditionalAddress
from devices.models import Device
from employees.models import Employee
from services.models import Service


class PriorityChoices(models.IntegerChoices):
    STANDARD = '0', 'Standard'
    URGENT = '1', 'Urgent'
    AD_HOC = '2', 'Ad Hoc'


class PaymentMethodChoices(models.IntegerChoices):
    PRO_INVOICE = '0', 'Pro Invoice'
    BANK_TRANSFER = '1', 'Bank Transfer'
    CASH = '2', 'Cash'


class OrderServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    price_net = models.FloatField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name} - {self.price_net} - {self.quantity}'


class Region(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ShortDescription(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Order(models.Model):
    user_intake = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='user_intake',
        verbose_name='Order Intake',
    )
    executor = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='executor_employee',
    )
    approver = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    additional_address = models.ForeignKey(
        AdditionalAddress,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    payer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='payer_customer',
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    short_description = models.ForeignKey(ShortDescription, on_delete=models.PROTECT, blank=True, null=True)
    additional_info = models.TextField(max_length=2000, blank=True, null=True)
    priority = models.SmallIntegerField(choices=PriorityChoices.choices, default=PriorityChoices.STANDARD)
    device_name = models.CharField(max_length=40, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)
    services = models.ManyToManyField(OrderServices, blank=True)
    payment_method = models.SmallIntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.BANK_TRANSFER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signer_name = models.CharField('Signer Name', max_length=20, blank=True, null=True)
    signature = JSignatureField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.payer:
            self.payer = self.customer
        super().save(*args, **kwargs)
