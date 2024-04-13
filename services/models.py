from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    device_brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Device Brand'),
    )
    device_model = models.ForeignKey(
        Model,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('Device Model'),
    )
    name = models.CharField(_('Name'), max_length=255)
    price_net = models.FloatField(_('Price Net'))
    description = models.TextField(_('Description'), max_length=300, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        name = ''
        if self.device_brand:
            name += f'{self.device_brand.name} '
        if self.device_model:
            name += f'{self.device_model.name} '
        if name:
            name += f'- {self.name} - {self.price_net} PLN'
        else:
            name = f'{self.name} - {self.price_net} PLN'
        return name
