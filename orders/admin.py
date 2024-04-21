from django.contrib import admin

from .models import Region, ShortDescription


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(ShortDescription)
class ShortDescriptionAdmin(admin.ModelAdmin):
    pass
