from django.db import models
from django.contrib.auth import get_user_model

from customers.models import Customer
from devices.models import Device
from employees.models import Employee
from services.models import Service


class PriorityChoices(models.IntegerChoices):
    STANDARD = '0', 'Standard'
    URGENT = '1', 'Urgent'
    AD_HOC = '2', 'Ad Hoc'


class PaymentMethodChoices(models.IntegerChoices):
    PRO_INVOICE = '0', 'Pro invoice'
    BANK_TRANSFER = '1', 'Bank transfer'
    CASH = '2', 'Cash'


class OrderServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    price_net = models.FloatField()
    quantity = models.PositiveSmallIntegerField()


class Region(models.Model):
    name = models.CharField(max_length=30)


class ShortDescription(models.Model):
    name = models.CharField(max_length=30)


class Order(models.Model):
    user_intake = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='user_intake')
    executor = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='executor_employee',
    )
    approver = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    invoice_number = models.CharField(max_length=20, blank=True, null=True)
    short_description = models.ForeignKey(ShortDescription, on_delete=models.PROTECT, blank=True, null=True)
    additional_info = models.TextField(max_length=2000, blank=True, null=True)
    priority = models.SmallIntegerField(choices=PriorityChoices.choices, default=PriorityChoices.STANDARD)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True)
    services = models.ManyToManyField(OrderServices)
    payment_method = models.SmallIntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.BANK_TRANSFER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
