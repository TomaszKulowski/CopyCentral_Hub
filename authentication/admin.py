from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


from .views import generate_password_reset_link


class CustomUserAdmin(UserAdmin):
    actions = ['send_password_reset_email']

    def send_password_reset_email(self, request, queryset):
        for user in queryset:
            reset_link = generate_password_reset_link(request, user.pk)

            subject = 'Reset Password'
            message = render_to_string('authentication/reset.html', {'reset_link': reset_link})
            recipient_list = [user.email]

            send_mail(subject, message, None, recipient_list)

    send_password_reset_email.short_description = _('Send password reset email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
