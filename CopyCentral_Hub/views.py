from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import activate
from django.views.generic import TemplateView

from .mixins import EmployeeRequiredMixin


class Home(EmployeeRequiredMixin, TemplateView):
    template_name = 'templates/base.html'


def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        activate(language)
        response = HttpResponseRedirect(reverse('home'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
