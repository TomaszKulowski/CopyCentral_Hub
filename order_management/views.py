from collections import defaultdict

from django.db.models import F, Case, Value, When, CharField, IntegerField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from employees.models import Employee
from orders.models import Order, PriorityChoices, PaymentMethodChoices, Region, OrderTypeChoices, StatusChoices


class OrderListViewBase(EmployeeRequiredMixin, ListView):
    model = Order
    template_name = ''
    context_object_name = 'orders'

    def get_queryset(self):
        orders = Order.objects.exclude(status__in=[2, 3, 4, 5]).values(
            'id',
            'status',
            'order_type',
            'priority',
            'created_at',
            'updated_at',
            'payment_method',
            'customer__id',
            'region__name',
            'short_description__name',
            'customer__name',
            executor_full_name=Concat(
                F('executor__user__first_name'),
                Value(' '),
                F('executor__user__last_name'),
                output_field=CharField()
            ),
            device_full_name=Case(
                When(device__isnull=False, then=Concat(
                    F('device__brand'), Value(', '),
                    F('device__model'), Value(', '),
                )),
                default=F('device_name'),
                output_field=CharField()
            ),
            address_full_name=Case(
                When(additional_address__isnull=False, then=Concat(
                    F('additional_address__city'), Value(', '),
                    F('additional_address__street'), Value(' '),
                    F('additional_address__number')
                )),
                default=Concat(
                    F('customer__billing_city'), Value(', '),
                    F('customer__billing_street'), Value(' '),
                    F('customer__billing_number')
                ),
                output_field=CharField(),
            ),
            order_intake_full_name=Concat(
                F('user_intake__user__first_name'),
                Value(' '),
                F('user_intake__user__last_name'),
                output_field=CharField()
            ),
        ).order_by('-id')

        status_map = {str(choice.value): choice.label for choice in StatusChoices}
        priority_map = {str(choice.value): choice.label for choice in PriorityChoices}
        order_type_map = {str(choice.value): choice.label for choice in OrderTypeChoices}
        payment_method_map = {str(choice.value): choice.label for choice in PaymentMethodChoices}

        for order in orders:
            order['status'] = status_map.get(str(order['status']), 'Unknown')
            order['priority'] = priority_map.get(str(order['priority']), 'Unknown')
            order['order_type'] = order_type_map.get(str(order['order_type']), 'Unknown')
            order['payment_method'] = payment_method_map.get(str(order['payment_method']), 'Unknown')

        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.pop('object_list', None)

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


class OrdersList(OrderListViewBase):
    template_name = 'order_management/main_order_management.html'


class EmployeesOrdersList(OrderListViewBase):
    template_name = 'order_management/employee_order_management.html'

    def get_queryset(self):
        orders = super().get_queryset()
        orders_dict = defaultdict(list)

        for order in orders:
            orders_dict[order['executor_full_name']].append(order)

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
