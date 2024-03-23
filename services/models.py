from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    device_brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    device_model = models.ForeignKey(
        Model,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    price_net = models.FloatField()
    description = models.TextField(max_length=300, blank=True, null=True)

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
