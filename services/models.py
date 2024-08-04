from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Brand(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    is_active = models.BooleanField(_('Is Active'), choices=[(True, 'True'), (False, 'False')], default=True)

    def __str__(self):
        if self.name == 'Basic Services':
            return f'{_("Basic Services ")}'
        return self.name


class Model(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    is_active = models.BooleanField(_('Is Active'), choices=[(True, 'True'), (False, 'False')], default=True)

    def __str__(self):
        if self.name == 'All Models':
            return f'{_("All Models")}'
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
    is_active = models.BooleanField(_('Is Active'), choices=[(True, 'True'), (False, 'False')], default=True)
    history = HistoricalRecords()

    def __str__(self):
        name = ''
        if self.device_brand.name == 'Basic Services':
            name += _('Basic Services ')
        elif self.device_brand:
            name += f'{self.device_brand.name} '
        if self.device_brand and not self.device_model and self.device_brand.name != 'Basic Services':
            name += _('- All Models')
        if self.device_model:
            if self.device_model.name:
                name += f'{self.device_model.name} '
        if name:
            if self.description:
                name += f'- {self.name} - [{self.description}] - {self.price_net} PLN'
            else:
                name += f'- {self.name} - {self.price_net} PLN'

        return name

    def save(self, *args, **kwargs):
        if not self.device_brand and not self.device_model:
            all_models_brand, created = Brand.objects.get_or_create(name='Basic Services')
            self.device_brand = all_models_brand
        super().save(*args, **kwargs)
