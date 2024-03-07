from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    price_net = models.FloatField()
    description = models.TextField(max_length=300, blank=True, null=True)
    device_brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Device Brand',
    )
    device_model = models.ForeignKey(
        Model,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Device Model',
    )
    device_type = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='Device Type',
    )
