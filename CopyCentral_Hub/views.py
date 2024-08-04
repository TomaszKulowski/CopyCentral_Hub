from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import activate
from django.views.generic import TemplateView
from django.shortcuts import render

from .mixins import EmployeeRequiredMixin
from informations.models import Information


class Home(EmployeeRequiredMixin, TemplateView):
    template_name = 'templates/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        informations = Information.objects.all()
        context['informations'] = informations

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)


def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        activate(language)
        response = HttpResponseRedirect(reverse('home'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

        return response
