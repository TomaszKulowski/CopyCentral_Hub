from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Model(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Service(models.Model):
    name = models.CharField(max_length=255)
    price_net = models.FloatField()
    description = models.TextField(max_length=300, blank=True, null=True)
    device_brand = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)
    device_model = models.ForeignKey(Model, on_delete=models.PROTECT, null=True, blank=True)
    device_type = models.ForeignKey(Type, on_delete=models.PROTECT, null=True, blank=True)
