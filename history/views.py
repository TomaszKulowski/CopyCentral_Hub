from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import View

from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from orders.models import OrderServices


class HistoryList(EmployeeRequiredMixin, View):
    template_name = 'history/history_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = {'history': {}}
        model = kwargs.get('model')
        model_id = kwargs.get('model_id')
        model_instance = model.objects.get(pk=model_id)
        context['model'] = model_instance

        history_queryset = model_instance.history.all()
        service_flag = True

        for index, entry in enumerate(history_queryset):
            if index < history_queryset.count() - 1:
                history_delta = entry.diff_against(history_queryset[index + 1])
                changed_fields = history_delta.changed_fields

                if not changed_fields:
                    continue

                history_entry = {
                    'history_details': {
                        'history_date': entry.history_date,
                        'employee': f'{entry.history_user.first_name} {entry.history_user.last_name}',
                    },
                }
                for field_name in changed_fields:
                    field_name_label = model._meta.get_field(field_name).verbose_name
                    n = 0
                    if field_name == 'services':
                        if service_flag:
                            service_flag = False
                            services = model_instance.services.all()
                            for service in services:
                                n += 1
                                services_history = service.history.all()
                                for service_index, service_entry in enumerate(services_history):
                                    if service_index < services_history.count() - 1:
                                        service_history_delta = service_entry.diff_against(services_history[service_index + 1])
                                        service_changed_fields = []
                                        for field in service_history_delta.changed_fields:
                                            service_changed_fields.append(str(service_entry.history_object._meta.get_field(field).verbose_name))

                                        if not service_changed_fields:
                                            continue

                                        service_history_entry = {
                                            'history_details': {
                                                'history_date': service_entry.history_date,
                                                'employee': f'{service_entry.history_user.first_name} {service_entry.history_user.last_name}',
                                            },
                                        }

                                        service_new_record = service_history_delta.new_record.instance
                                        service_old_record = service_history_delta.old_record.instance

                                        service_changes = {', '.join(service_changed_fields): [service_new_record, service_old_record]}
                                        service_history_entry.update(service_changes)

                                        context['history']['0' + str(n) + str(service_index)] = service_history_entry

                        if 'services' in changed_fields:
                            new_record = history_delta.changes[0].new
                            old_record = history_delta.changes[0].old
                            new_value = [item for item in new_record if item not in old_record]
                            old_value = [item for item in old_record if item not in new_record]

                            if new_value:
                                service_id = new_value[0]['orderservices']
                                new_service = get_object_or_404(OrderServices, pk=service_id)
                            else:
                                new_service = '---'
                            if old_value:
                                service_id = old_value[0]['orderservices']
                                old_service = get_object_or_404(OrderServices, pk=service_id)
                            else:
                                old_service = '---'

                            changes = {field_name_label: [new_service, old_service]}
                            history_entry.update(changes)
                            continue

                    new_record = getattr(history_delta.new_record, field_name)
                    old_record = getattr(history_delta.old_record, field_name)

                    changes = {field_name_label: [new_record, old_record]}
                    history_entry.update(changes)

                context['history'][str(index)] = history_entry

        sorted_context = sorted(
            context['history'].items(),
            key=lambda x: x[1]['history_details']['history_date'], reverse=True
        )

        paginator = Paginator(sorted_context, self.paginate_by)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['history'] = page_obj

        return context

    def get_model(self, model_name):
        try:
            app_config = apps.get_app_config(model_name)
        except LookupError:
            return False

        for model in app_config.get_models():
            content_type = ContentType.objects.get_for_model(model)
            if content_type:
                # models with support history
                if content_type.name in ['device', 'customer', 'order', 'orderservices', 'service']:
                    return model
        return False

    def get(self, request):
        model = self.get_model(request.GET.get('model'))
        model_id = request.GET.get('model_id')
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            'previous_url': previous_url,
            'model_name': request.GET.get('model'),
            'model_id': model_id,
        }
        if model:
            context.update(self.get_context_data(model=model, model_id=model_id))
            return render(request, template_name=self.template_name, context=context)

        return HttpResponseBadRequest()
