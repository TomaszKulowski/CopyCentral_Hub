from django.db import models
from django.utils.translation import gettext_lazy as _


class Information(models.Model):
    information = models.TextField(_('Information'), blank=True, null=True, max_length=12000)

    def __str__(self):
        return str(self.information)
