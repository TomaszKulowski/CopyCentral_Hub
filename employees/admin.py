from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ['user', 'department']
    list_display = ['user', 'department']
