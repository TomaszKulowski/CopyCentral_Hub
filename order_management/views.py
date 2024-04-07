from collections import defaultdict

from django.db.models import F, Case, Value, When, CharField, IntegerField
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from CopyCentral_Hub.mixins import EmployeeRequiredMixin
from employees.models import Employee
from orders.models import Order, PriorityChoices, Region
from orders.utils import map_choices_int_to_str


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
            'sort_number',
            'executor__id',
            additional_info_name=Case(
                When(additional_info__isnull=False, then=F('additional_info')),
                default=Value('---'),
                output_field=CharField()
            ),
            description_name=Case(
                When(description__isnull=False, then=F('description')),
                default=Value('---'),
                output_field=CharField()
            ),
            short_description_name=Case(
                When(short_description__name__isnull=False, then=F('short_description__name')),
                default=Value('---'),
                output_field=CharField()
            ),
            customer_name=Case(
                When(customer__name__isnull=False, then=F('customer__name')),
                default=Value('---'),
                output_field=CharField()
            ),
            executor_name=Concat(
                F('executor__user__first_name'),
                Value(' '),
                F('executor__user__last_name'),
                output_field=CharField()
            ),
            device_full_name=Case(
                When(device__brand__isnull=False, then=Concat(
                    F('device__brand'), Value(', '),
                    F('device__model'),
                )),
                When(device_name__isnull=False, then=F('device_name')),
                default=Value('---'),
                output_field=CharField()
            ),
            address_name=Case(
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
            order_intake_name=Concat(
                F('user_intake__user__first_name'),
                Value(' '),
                F('user_intake__user__last_name'),
                output_field=CharField()
            ),
        ).order_by('-id')

        return orders

    def get_context_data(self, **kwargs):
        orders = self.get_queryset()
        orders = map_choices_int_to_str(orders)

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

        context = {
            'orders': orders,
            'employees': employees,
            'regions': regions,
            'priorities': priorities,
            'selected_region': self.request.session.get('selected_region', 'Display All')
        }

        return context


class OrdersList(OrderListViewBase):
    template_name = 'order_management/main_order_management.html'


class EmployeesOrdersList(OrderListViewBase):
    template_name = 'order_management/employees_order_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = map_choices_int_to_str(self.get_queryset().order_by('sort_number'))
        orders_dict = defaultdict(list)

        for order in orders:
            if order['executor_name'] and order['executor_name'] != ' ':
                orders_dict[order['executor_name']].append(order)

        result = []
        for executor, orders in orders_dict.items():
            result.append({
                'executor': executor,
                'orders_list': orders
            })
        result_sorted = sorted(result, key=lambda x: x['executor'])
        context['orders'] = result_sorted

        return context


class RegionsOrdersList(OrderListViewBase):
    template_name = 'order_management/regions_order_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders_dict = defaultdict(list)

        for order in context['orders']:
            if not order['region__name']:
                orders_dict['None'].append(order)
            else:
                orders_dict[order['region__name']].append(order)

        result = []
        for region, orders in orders_dict.items():
            result.append({
                'region': region,
                'orders_list': orders
            })
        result_sorted = sorted(result, key=lambda x: x['region'])
        context['orders'] = result_sorted

        return context


class MyOrdersList(EmployeesOrdersList):
    template_name = 'order_management/my_orders_management.html'

    def get_queryset(self):
        orders = super().get_queryset()
        employee_instance = get_object_or_404(Employee, user=self.request.user)
        orders = orders.filter(executor_id=employee_instance.id).order_by('sort_number')

        return orders

    def get_context_data(self, **kwargs):
        orders = map_choices_int_to_str(self.get_queryset())
        orders_dict = defaultdict(list)

        for order in orders:
            if not order['region__name']:
                orders_dict['None'].append(order)
            else:
                orders_dict[order['region__name']].append(order)

        result = []
        for region, orders in orders_dict.items():
            result.append({
                'region': region,
                'orders_list': orders
            })
        result_sorted = sorted(result, key=lambda x: x['region'])
        context = {
            'orders': result_sorted,
            'selected_region': self.request.session.get('selected_region', 'Display All'),
        }

        return context


class ApplyFilters(EmployeeRequiredMixin, View):
    def get(self, request):
        if 'region' in request.GET:
            request.session['selected_region'] = request.GET.get('region')
        return JsonResponse({'status': 200})
