from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords


class Type(models.IntegerChoices):
    MONO = 0, _('Monochrome')
    COLOR = 1, _('Color')


class Format(models.IntegerChoices):
    A4 = 0, _('A4')
    A3 = 1, _('A3')


class Status(models.IntegerChoices):
    AVAILABLE = 0, _('Available')
    UNAVAILABLE = 1, _('Unavailable')
    RESERVED = 2, _('Reserved')
    LEASED = 3, _('Leased')
    SOLD = 4, _('Sold')
    REPLACEMENT = 5, _('Replacement')
    IN_DELIVERY_INVISIBLE = 6, _('In delivery INVISIBLE')
    IN_DELIVERY = 7, _('In delivery')
    SERVICED = 8, _('Serviced')


class Device(models.Model):
    brand = models.CharField(_('Brand'), max_length=30)
    model = models.CharField(_('Model'), max_length=50)
    serial_number = models.CharField(_('Serial Number'), max_length=40, unique=True)
    type = models.SmallIntegerField(_('Type'), choices=Type.choices, blank=True, null=True)
    format = models.SmallIntegerField(_('Format'), choices=Format.choices, blank=True, null=True)
    total_counter = models.IntegerField(_('Total Counter'), blank=True, null=True)
    mono_counter = models.IntegerField(_('Mono Counter'), blank=True, null=True)
    color_counter = models.IntegerField(_('Color Counter'), blank=True, null=True)
    description = models.TextField(_('Description'), max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(_('Status'), choices=Status.choices, blank=True, null=True)
    price_net = models.FloatField(_('Price Net'), blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Device')

    def __str__(self):
        return f'{self.brand} {self.model}; {self.serial_number}'
