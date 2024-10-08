from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class DepartmentChoices(models.IntegerChoices):
    BOSS = 0, _('Boss')
    MANAGER = 1, _('Manager')
    OFFICE = 2, _('Office staff')
    TECHNICIAN = 3, _('Technician')
    SELLER = 4, _('Seller')
    WAREHOUSE = 5, _('Warehouse staff')


class Employee(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='employee',
        verbose_name=_('User'),
    )
    department = models.SmallIntegerField(_('Department'), choices=DepartmentChoices.choices)
    phone_number = models.PositiveBigIntegerField(_('Phone Number'), blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
