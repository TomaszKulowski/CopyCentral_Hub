from django.views.generic import TemplateView

from .mixins import EmployeeRequiredMixin


class Home(EmployeeRequiredMixin, TemplateView):
    template_name = 'templates/base.html'
