from django.contrib.auth import get_user_model
from django.db import models


class DepartmentChoices(models.IntegerChoices):
    BOSS = (0, 'Boss')
    MANAGER = (1, 'Manager')
    OFFICE = (2, 'Office staff')
    TECHNICIAN = (3, 'Technician')
    SELLER = (4, 'Seller')
    WAREHOUSE = (5, 'Warehouse staff')


class Employee(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='employee')
    department = models.SmallIntegerField(choices=DepartmentChoices.choices)

    def __str__(self):
        return self.user.username
