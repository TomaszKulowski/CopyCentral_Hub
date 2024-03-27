from collections import defaultdict

from django.db.models import F, Case, Value, When, CharField, IntegerField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from employees.models import Employee
from orders.models import PriorityChoices, PaymentMethodChoices, Region
from service_orders.models import ServiceOrder, OrderType, Status


class OrdersList(EmployeeRequiredMixin, ListView):
    model = ServiceOrder
    template_name = 'order_management/main_order_management.html'
    context_object_name = 'orders'

    def get_queryset(self):
        orders = ServiceOrder.objects.exclude(status__in=[2, 3, 4, 5]).values(
            'id',
            'order__id',
            'status',
            'order_type',
            region=F('order__region__name'),
            customer=F('order__customer__name'),
            customer_id=F('order__customer__id'),
            priority=F('order__priority'),
            short_description=F('order__short_description__name'),
            executor=Concat(
                F('order__executor__user__first_name'),
                Value(' '),
                F('order__executor__user__last_name'),
                output_field=CharField()
            ),
            device=Case(
                When(order__device__isnull=False, then=Concat(
                    F('order__device__brand'), Value(', '),
                    F('order__device__model'), Value(', '),
                )),
                default=F('order__device_name'),
                output_field=CharField()
            ),
            address=Case(
                When(order__additional_address__isnull=False, then=Concat(
                    F('order__additional_address__city'), Value(', '),
                    F('order__additional_address__street'), Value(' '),
                    F('order__additional_address__number')
                )),
                default=Concat(
                    F('order__customer__billing_city'), Value(', '),
                    F('order__customer__billing_street'), Value(' '),
                    F('order__customer__billing_number')
                ),
                output_field=CharField(),
            ),
            order_intake=Concat(
                F('order__user_intake__user__first_name'),
                Value(' '),
                F('order__user_intake__user__last_name'),
                output_field=CharField()
            ),
            created_at=F('order__created_at'),
            updated_at=F('order__updated_at'),
            payment_method=F('order__payment_method'),
        ).order_by('-id')

        status_map = {str(choice.value): choice.label for choice in Status}
        priority_map = {str(choice.value): choice.label for choice in PriorityChoices}
        order_type_map = {str(choice.value): choice.label for choice in OrderType}
        payment_method_map = {str(choice.value): choice.label for choice in PaymentMethodChoices}

        for order in orders:
            order['status'] = status_map.get(str(order['status']), 'Unknown')
            order['priority'] = priority_map.get(str(order['priority']), 'Unknown')
            order['order_type'] = order_type_map.get(str(order['order_type']), 'Unknown')
            order['payment_method'] = payment_method_map.get(str(order['payment_method']), 'Unknown')

        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employees = Employee.objects.annotate(
            full_name=Concat(F('user__first_name'), Value(' '), F('user__last_name'), output_field=CharField())
        ).order_by(
            Case(
                When(department=3, then=0),
                default=1,
                output_field=IntegerField()
            ),
            'department'
        ).values('id', 'full_name', 'department')
        regions = Region.objects.all()
        priorities = PriorityChoices.choices

        context['employees'] = employees
        context['regions'] = regions
        context['priorities'] = priorities

        context['selected_region'] = self.request.session.get('selected_region', 'Display All')

        return context


class EmployeesOrdersList(EmployeeRequiredMixin, ListView):
    model = ServiceOrder
    template_name = 'order_management/employee_order_management.html'
    context_object_name = 'orders'

    def get_queryset(self):
        orders = ServiceOrder.objects.exclude(status__in=[2, 3, 4, 5]).values(
            'id',
            'order__id',
            'status',
            'order_type',
            region=F('order__region__name'),
            customer=F('order__customer__name'),
            customer_id=F('order__customer__id'),
            priority=F('order__priority'),
            short_description=F('order__short_description__name'),
            executor=Concat(
                F('order__executor__user__first_name'),
                Value(' '),
                F('order__executor__user__last_name'),
                output_field=CharField()
            ),
            device=Case(
                When(order__device__isnull=False, then=Concat(
                    F('order__device__brand'), Value(', '),
                    F('order__device__model'), Value(', '),
                )),
                default=F('order__device_name'),
                output_field=CharField()
            ),
            address=Case(
                When(order__additional_address__isnull=False, then=Concat(
                    F('order__additional_address__city'), Value(', '),
                    F('order__additional_address__street'), Value(' '),
                    F('order__additional_address__number')
                )),
                default=Concat(
                    F('order__customer__billing_city'), Value(', '),
                    F('order__customer__billing_street'), Value(' '),
                    F('order__customer__billing_number')
                ),
                output_field=CharField(),
            ),
            order_intake=Concat(
                F('order__user_intake__user__first_name'),
                Value(' '),
                F('order__user_intake__user__last_name'),
                output_field=CharField()
            ),
            created_at=F('order__created_at'),
            updated_at=F('order__updated_at'),
            payment_method=F('order__payment_method'),
        )

        orders_dict = defaultdict(list)
        status_map = {str(choice.value): choice.label for choice in Status}
        priority_map = {str(choice.value): choice.label for choice in PriorityChoices}
        order_type_map = {str(choice.value): choice.label for choice in OrderType}
        payment_method_map = {str(choice.value): choice.label for choice in PaymentMethodChoices}

        for order in orders:
            order['status'] = status_map.get(str(order['status']), 'Unknown')
            order['priority'] = priority_map.get(str(order['priority']), 'Unknown')
            order['order_type'] = order_type_map.get(str(order['order_type']), 'Unknown')
            order['payment_method'] = payment_method_map.get(str(order['payment_method']), 'Unknown')

            orders_dict[order['executor']].append(order)

        result = []
        for executor, orders in orders_dict.items():
            if executor == ' ':
                continue
            result.append({
                'executor': executor,
                'orders_list': orders

            })

        return result


class ApplyFilters(EmployeeRequiredMixin, View):
    def get(self, request):
        if 'region' in request.GET:
            request.session['selected_region'] = request.GET.get('region')
        return JsonResponse({'status': 200})
