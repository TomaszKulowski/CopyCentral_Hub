from django.db import models

from orders.models import Order


class OrderType(models.IntegerChoices):
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


class Status(models.IntegerChoices):
    NEW = '0', 'New'
    IN_PROGRESS = '1', 'In Progress'
    CANCELED = '2', 'Canceled'
    SETTLED = '3', 'Settled'
    COMPLETED = '4', 'Completed'
    SHIPPED = '5', 'Shipped'
    AWAITING_DELIVERY = '6', 'Awaiting Delivery'
    AWAITING_PAYMENT = '7', 'Awaiting Payment'
    AWAITING_PICKUP = '8', 'Awaiting Pickup'


class ServiceOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    description = models.TextField(max_length=2000, blank=True, null=True)
    order_type = models.SmallIntegerField(choices=OrderType.choices, default=OrderType.PAID)
    status = models.SmallIntegerField(choices=Status.choices, default=Status.NEW)
    total_counter = models.PositiveIntegerField(blank=True, null=True)
    mono_counter = models.PositiveIntegerField(blank=True, null=True)
    color_counter = models.PositiveIntegerField(blank=True, null=True)
