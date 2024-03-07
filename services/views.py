from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import UpdateView, CreateView

from contractors.forms import ContractorForm
from .models import Service
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class ServicesList(EmployeeRequiredMixin, View):
    def get(self, request):
        services = Service.objects.all()
        search_query = request.GET.get('search', False)

        if search_query:
            services = services.filter(
                Q(name__icontains=search_query) |
                Q(description__first_name__icontains=search_query)
            )

        page = request.GET.get('page')
        paginator = Paginator(services, 10)
        page_obj = paginator.get_page(page)

        if search_query or search_query == '':
            return render(request, 'services/list_table.html', {'page_obj': page_obj})

        return render(request, 'services/list.html', {'page_obj': page_obj})


class ServiceDetails(EmployeeRequiredMixin, UpdateView):
    model = Service
    template_name = 'contractors/details.html'
    form_class = ContractorForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        forms = {}
        for key, value in form.fields.items():
            value.disabled = True
            forms[key] = value
        return form


class ServiceUpdate(EmployeeRequiredMixin, UpdateView):
    model = Service
    template_name = 'contractors/update.html'
    form_class = ContractorForm

    def get_success_url(self):
        return reverse_lazy('contractors:details', kwargs={'pk': self.object.pk})


class ServiceCreate(EmployeeRequiredMixin, CreateView):
    model = Service
    form_class = ContractorForm

    def get_success_url(self):
        return reverse_lazy('contractors:details', kwargs={'pk': self.object.pk})
