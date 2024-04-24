from django.contrib.auth import get_user_model
from django.db import models

from orders.models import Order


class OrderReview(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False, blank=True, null=True)
    for_review = models.BooleanField(default=False, blank=True, null=True)
