from django.core.cache import cache
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .tasks import notifications_task
from .models import Notification, NotificationSettings
from .utils import mark_orders_as_sent


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    change_list_template = 'notifications/templates/notifications/settings.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_notifications/', self.admin_site.admin_view(self.send_notifications), name='send_notifications'),
        ]
        return custom_urls + urls

    def send_notifications(self, request):
        if not cache.get('notification_enabled'):
            mark_orders_as_sent()
            notifications_task.delay()
            cache.set('notification_enabled', True, timeout=None)
            self.message_user(request, _('Notification enabled'))
        else:
            self.message_user(request, _('Notifications are already enabled'))

        return HttpResponseRedirect("../")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['send_notifications_url'] = 'send_notifications/'

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['receiver_name', 'phone_number', 'message', 'sent', 'created_at']
    search_fields = ['receiver_name', 'phone_number']
    list_per_page = 20

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
