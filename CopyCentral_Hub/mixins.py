from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class EmployeeRequiredMixin(AccessMixin):
    """
    Mixin that requires the user to be employee.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.employee.first():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('authentication:login'))


class OfficeWorkerRequiredMixin(EmployeeRequiredMixin):
    """
    Mixin that requires the user to be office worker.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.employee.first().department <= 2:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
