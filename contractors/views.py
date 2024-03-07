from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import UpdateView, CreateView

from .forms import ContractorForm
from .models import Contractor
from CopyCentral_Hub.mixins import EmployeeRequiredMixin


class ContractorsList(EmployeeRequiredMixin, View):
    def get(self, request):
        contractors = Contractor.objects.all()
        search_query = request.GET.get('search', False)

        if search_query:
            contractors = contractors.filter(
                Q(name__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(tax__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(street__icontains=search_query)
            )

        page = request.GET.get('page')
        paginator = Paginator(contractors, 10)
        page_obj = paginator.get_page(page)

        if search_query or search_query == '':
            return render(request, 'contractors/list_table.html', {'page_obj': page_obj})

        return render(request, 'contractors/list.html', {'page_obj': page_obj})


class ContractorDetails(EmployeeRequiredMixin, UpdateView):
    model = Contractor
    template_name = 'contractors/details.html'
    form_class = ContractorForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        forms = {}
        for key, value in form.fields.items():
            value.disabled = True
            forms[key] = value
        return form


class ContractorUpdate(EmployeeRequiredMixin, UpdateView):
    model = Contractor
    template_name = 'contractors/update.html'
    form_class = ContractorForm

    def get_success_url(self):
        return reverse_lazy('contractors:details', kwargs={'pk': self.object.pk})


class ContractorCreate(EmployeeRequiredMixin, CreateView):
    model = Contractor
    template_name = 'contractors/update.html'
    form_class = ContractorForm

    def get_success_url(self):
        return reverse_lazy('contractors:details', kwargs={'pk': self.object.pk})
