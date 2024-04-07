from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.shortcuts import get_object_or_404
from jsignature.fields import JSignatureField
from pathlib import Path
from sorl.thumbnail import ImageField

from customers.models import Customer, AdditionalAddress
from devices.models import Device
from employees.models import Employee
from services.models import Service


def validate_file_size(value):
    filesize = value.size

    if filesize > (40 * 1024 * 1024):
        raise ValidationError("The maximum file size that can be uploaded is 40MB")


def upload_to(instance, filename):
    return Path().joinpath('attachments', str(instance.id), filename)


class StatusChoices(models.IntegerChoices):
    NEW = '0', 'New'
    IN_PROGRESS = '1', 'In Progress'
    CANCELED = '2', 'Canceled'
    SETTLED = '3', 'Settled'
    COMPLETED = '4', 'Completed'
    SHIPPED = '5', 'Shipped'
    AWAITING_DELIVERY = '6', 'Awaiting Delivery'
    AWAITING_PAYMENT = '7', 'Awaiting Payment'
    AWAITING_PICKUP = '8', 'Awaiting Pickup'


class OrderTypeChoices(models.IntegerChoices):
    FREE = '0', 'Free'
    PAID = '1', 'Paid'
    WARRANTY = '2', 'Warranty'
    COMPLAINT = '3', 'Complaint'
    LEASE = '4', 'Lease'
    FREE_TO_CONFIRM = '5', 'Free - To Confirm'
    PAID_TO_CONFIRM = '6', 'Paid - To Confirm'
    WARRANTY_TO_CONFIRM = '7', 'Warranty - To Confirm'
    COMPLAINT_TO_CONFIRM = '8', 'Complaint - To Confirm'
    LEASE_TO_CONFIRM = '9', 'Lease - To Confirm'


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
    description = models.TextField(max_length=2000, blank=True, null=True)
    order_type = models.SmallIntegerField(choices=OrderTypeChoices.choices, default=OrderTypeChoices.PAID)
    status = models.SmallIntegerField(choices=StatusChoices.choices, default=StatusChoices.NEW)
    total_counter = models.PositiveIntegerField(blank=True, null=True)
    mono_counter = models.PositiveIntegerField(blank=True, null=True)
    color_counter = models.PositiveIntegerField(blank=True, null=True)
    services = models.ManyToManyField(OrderServices, blank=True)
    payment_method = models.SmallIntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.BANK_TRANSFER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signer_name = models.CharField('Signer Name', max_length=20, blank=True, null=True)
    signature = JSignatureField(blank=True, null=True)
    sort_number = models.SmallIntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.description == '':
            self.description = None
        if self.additional_info == '':
            self.additional_info = None

        if not self._state.adding:
            old_order_instance = get_object_or_404(Order, pk=self.pk)
            if old_order_instance.executor:
                if self.status in [2, 3, 4, 5]:
                    self.sort_number = None
                    Order.objects.filter(
                        executor=old_order_instance.executor,
                        sort_number__gt=old_order_instance.sort_number
                    ).update(sort_number=models.F('sort_number') - 1)

                if old_order_instance.executor != self.executor:
                    if self.executor is not None:
                        max_sort_number_new_executor = Order.objects.filter(
                            executor=self.executor
                        ).aggregate(Max('sort_number'))['sort_number__max']
                        if max_sort_number_new_executor:
                            self.sort_number = max_sort_number_new_executor + 1
                        else:
                            self.sort_number = 1
                    else:
                        self.sort_number = None
                    Order.objects.filter(
                        executor=old_order_instance.executor,
                        sort_number__gt=old_order_instance.sort_number
                    ).update(sort_number=models.F('sort_number') - 1)
            else:
                if self.executor:
                    self.sort_number = 1

        if self._state.adding and self.executor:
            max_sort_number = Order.objects.filter(
                executor=self.executor
            ).aggregate(Max('sort_number'))['sort_number__max']
            if max_sort_number is not None:
                self.sort_number = max_sort_number + 1
            else:
                self.sort_number = 1

        if not self.payer:
            self.payer = self.customer
        super().save(*args, **kwargs)


class Attachment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    image = ImageField(upload_to=upload_to, max_length=150, blank=True, null=True, validators=[validate_file_size])
    file = models.FileField(upload_to=upload_to, max_length=150, blank=True, null=True, validators=[validate_file_size])
