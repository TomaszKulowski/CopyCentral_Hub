from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InformationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'informations'
    verbose_name = _('information')
