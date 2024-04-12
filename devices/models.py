from django.db import models

from simple_history.models import HistoricalRecords


class Type(models.IntegerChoices):
    MONO = 0, 'Monochrome'
    COLOR = 1, 'Color'


class Format(models.IntegerChoices):
    A4 = 0, 'A4'
    A3 = 1, 'A3'


class Status(models.IntegerChoices):
    AVAILABLE = 0, 'Available'
    UNAVAILABLE = 1, 'Unavailable'
    RESERVED = 2, 'Reserved'
    LEASED = 3, 'Leased'
    SOLD = 4, 'Sold'
    REPLACEMENT = 5, 'Replacement'
    IN_DELIVERY_INVISIBLE = 6, 'In delivery INVISIBLE'
    IN_DELIVERY = 7, 'In delivery'
    SERVICED = 8, 'Serviced'


class Device(models.Model):
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    serial_number = models.CharField('Serial Number', max_length=40, unique=True, blank=True, null=True)
    type = models.SmallIntegerField(choices=Type.choices, blank=True, null=True)
    format = models.SmallIntegerField(choices=Format.choices, blank=True, null=True)
    total_counter = models.IntegerField(blank=True, null=True)
    mono_counter = models.IntegerField(blank=True, null=True)
    color_counter = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(choices=Status.choices, blank=True, null=True)
    price_net = models.FloatField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.brand} {self.model}; {self.serial_number}'
