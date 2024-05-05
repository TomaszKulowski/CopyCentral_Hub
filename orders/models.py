from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from jsignature.fields import JSignatureField
from pathlib import Path
from sorl.thumbnail import ImageField
from simple_history.models import HistoricalRecords

from customers.models import Customer, AdditionalAddress
from devices.models import Device
from employees.models import Employee
from services.models import Service


def validate_file_size(value):
    filesize = value.size

    if filesize > (40 * 1024 * 1024):
        raise ValidationError(_("The maximum file size that can be uploaded is 40MB"))


def upload_to(instance, filename):
    return Path().joinpath('attachments', str(instance.id), filename)


class StatusChoices(models.IntegerChoices):
    NEW = 0, _('New')
    IN_PROGRESS = 1, _('In Progress')
    CANCELED = 2, _('Canceled')
    SETTLED = 3, _('Settled')
    COMPLETED = 4, _('Completed')
    SHIPPED = 5, _('Shipped')
    AWAITING_DELIVERY = 6, _('Awaiting Delivery')
    AWAITING_PAYMENT = 7, _('Awaiting Payment')
    AWAITING_PICKUP = 8, _('Awaiting Pickup')


class OrderTypeChoices(models.IntegerChoices):
    FREE = 0, _('Free')
    PAID = 1, _('Paid')
    WARRANTY = 2, _('Warranty')
    COMPLAINT = 3, _('Complaint')
    LEASE = 4, _('Lease')
    FREE_TO_CONFIRM = 5, _('Free - To Confirm')
    PAID_TO_CONFIRM = 6, _('Paid - To Confirm')
    WARRANTY_TO_CONFIRM = 7, _('Warranty - To Confirm')
    COMPLAINT_TO_CONFIRM = 8, _('Complaint - To Confirm')
    LEASE_TO_CONFIRM = 9, _('Lease - To Confirm')


class PriorityChoices(models.IntegerChoices):
    STANDARD = 0, _('Standard')
    URGENT = 1, _('Urgent')
    AD_HOC = 2, _('Ad Hoc')


class PaymentMethodChoices(models.IntegerChoices):
    PRO_INVOICE = 0, _('Pro Invoice')
    BANK_TRANSFER = 1, _('Bank Transfer')
    CASH = 2, _('Cash')


class OrderService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name=_('Service'), blank=True, null=True)
    name = models.CharField(_('Name'), max_length=255)
    price_net = models.FloatField(_('Price Net'))
    quantity = models.PositiveSmallIntegerField(_('Quantity'))
    from_session = models.BooleanField(default=True, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return _('Name') + f': {self.name} - ' + _('Net Price') + f': {self.price_net} - ' + _('Qty') + f': {self.quantity}'

    def save(self, *args, **kwargs):
        self.from_session = False
        super().save(*args, **kwargs)


class Region(models.Model):
    name = models.CharField(_('Name'), max_length=30)

    def __str__(self):
        return self.name


class ShortDescription(models.Model):
    name = models.CharField(_('Name'), max_length=30)

    def __str__(self):
        return self.name


class Order(models.Model):
    user_intake = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='user_intake',
        verbose_name=_('Order Intake'),
    )
    executor = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='executor_employee',
        verbose_name=_('Executor'),
    )
    approver = models.ForeignKey(Employee, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Approver'))
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Customer'))
    phone_number = models.IntegerField(_('Phone Number'), blank=True, null=True)
    additional_address = models.ForeignKey(
        AdditionalAddress,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Additional Address'),
    )
    payer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='payer_customer',
        verbose_name=_('Payer'),
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Region'))
    invoice_number = models.CharField(_('Invoice Number'), max_length=20, blank=True, null=True)
    short_description = models.ForeignKey(
        ShortDescription,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('Short Description'),
    )
    additional_info = models.TextField(_('Additional Info'), max_length=2000, blank=True, null=True)
    priority = models.SmallIntegerField(_('Priority'), choices=PriorityChoices.choices, default=PriorityChoices.STANDARD)
    device_name = models.CharField(_('Device Name'), max_length=40, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Device'))
    description = models.TextField(_('Description'), max_length=2000, blank=True, null=True)
    order_type = models.SmallIntegerField(_('Order Type'), choices=OrderTypeChoices.choices, default=OrderTypeChoices.PAID)
    status = models.SmallIntegerField(_('Status'), choices=StatusChoices.choices, default=StatusChoices.NEW)
    total_counter = models.PositiveIntegerField(_('Total Counter'), blank=True, null=True)
    mono_counter = models.PositiveIntegerField(_('Mono Counter'), blank=True, null=True)
    color_counter = models.PositiveIntegerField(_('Color Counter'), blank=True, null=True)
    services = models.ManyToManyField(OrderService, blank=True, verbose_name=_('Services'))
    payment_method = models.SmallIntegerField(
        _('Payment Method'),
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.BANK_TRANSFER
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    signer_name = models.CharField(_('Signer Name'), max_length=20, blank=True, null=True)
    signature = JSignatureField(_('Signature'), blank=True, null=True)
    sort_number = models.SmallIntegerField(_('Sort Number'), blank=True, null=True)
    history = HistoricalRecords(m2m_fields=[services])

    def __str__(self):
        return _('Order ID') + f' {self.id}'

    def save(self, *args, **kwargs):
        if self.description == '':
            self.description = None
        if self.additional_info == '':
            self.additional_info = None

        if not self._state.adding:
            old_order_instance = get_object_or_404(Order, pk=self.pk)
            if old_order_instance.executor:
                if self.status in [0, 1, 6, 7, 8] and not old_order_instance.sort_number:
                    if self.executor:
                        max_sort_number = Order.objects.filter(
                            executor=self.executor
                        ).aggregate(Max('sort_number'))['sort_number__max']
                        if max_sort_number:
                            self.sort_number = max_sort_number + 1
                        else:
                            self.sort_number = 1

                elif self.status in [2, 3, 4, 5] and old_order_instance.sort_number:
                    self.sort_number = None
                    Order.objects.filter(
                        executor=old_order_instance.executor,
                        sort_number__gt=old_order_instance.sort_number
                    ).update(sort_number=models.F('sort_number') - 1)

                elif old_order_instance.executor != self.executor and self.status not in [2, 3, 4, 5]:
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

                    if self.sort_number and old_order_instance.sort_number:
                        Order.objects.filter(
                            executor=old_order_instance.executor,
                            sort_number__gt=old_order_instance.sort_number
                        ).update(sort_number=models.F('sort_number') - 1)
                else:
                    if old_order_instance.sort_number and not self.sort_number:
                        self.sort_number = old_order_instance.sort_number
            else:
                if self.status not in [2, 3, 4, 5]:
                    if self.executor:
                        max_sort_number = Order.objects.filter(
                            executor=self.executor
                        ).aggregate(Max('sort_number'))['sort_number__max']
                        if max_sort_number:
                            self.sort_number = max_sort_number + 1
                        else:
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
        if self.customer:
            if not self.phone_number:
                customer = get_object_or_404(Customer, pk=self.customer.id)
                self.phone_number = customer.phone_number
        super().save(*args, **kwargs)


class Attachment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name=_('Order'))
    image = ImageField(_('Image'), upload_to=upload_to, max_length=150, blank=True, null=True, validators=[validate_file_size])
    file = models.FileField(_('File'), upload_to=upload_to, max_length=150, blank=True, null=True, validators=[validate_file_size])
