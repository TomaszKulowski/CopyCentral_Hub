from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypeChoices(models.IntegerChoices):
    NEW_ORDER = 0, _('New Order')


class NotificationSettings(models.Model):
    server = models.CharField(max_length=300)
    auth_token = models.CharField(max_length=300)
    message_template = models.TextField(max_length=300, help_text='"$orders_ids" will be replaced by the order ID')
    notification_type = models.SmallIntegerField(
        choices=NotificationTypeChoices.choices,
        unique=True,
    )
    delay_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Time in minutes before the message is sent',
    )

    class Meta:
        verbose_name = _('notification setting')
        verbose_name_plural = _('notification settings')

    def __str__(self):
        return f'{_("Notification type")}: {self.get_notification_type_display()}'


class Notification(models.Model):
    settings = models.ForeignKey(NotificationSettings, on_delete=models.PROTECT, blank=True, null=True)
    receiver_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    message = models.TextField(max_length=400, blank=True, null=True)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
