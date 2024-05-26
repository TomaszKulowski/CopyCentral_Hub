from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Sum, Q
from django.shortcuts import get_object_or_404, render
from django.views import View


from .models import OrderReview
from CopyCentral_Hub.mixins import OfficeWorkerRequiredMixin
from orders.models import Order


class OrderReviewList(OfficeWorkerRequiredMixin, View):
    template_name = 'order_review/order_review.html'
    template_table_name = 'order_review/order_review_table.html'
    paginate_by = 10

    def get_queryset(self):
        for_review = self.request.GET.get('for_review')
        if for_review:
            orders = Order.objects.filter(
                orderreview__user_id=self.request.user.id,
                orderreview__is_approved=False,
                orderreview__for_review=True,
            )

        else:
            orders = Order.objects.filter(
                orderreview__user_id=self.request.user.id,
                orderreview__is_approved=False,
                orderreview__for_review=False,
            )

        orders = orders.filter(status__in=[2, 3, 4, 5]).prefetch_related('services').order_by('-updated_at')

        return orders

    def get_context_data(self, **kwargs):
        context = {}
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        for_review = self.request.GET.get('for_review')

        if for_review:
            context['for_review'] = 'true'

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        for order in context['page_obj']:
            order.active_services = order.services.filter(is_active=True)
            total_price = order.active_services.aggregate(total_price=Sum(F('price_net') * F('quantity')))['total_price']
            order.total_price = total_price if total_price else 0

        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context=context)

    def post(self, request):
        action_type = request.POST.get('action_type')
        order_id = request.POST.get('order_id')
        order_instance = get_object_or_404(Order, pk=order_id)
        order_review_instance = OrderReview.objects.filter(user=request.user, order=order_instance).first()

        if not order_review_instance:
            order_review_instance = OrderReview.objects.create(user=request.user, order=order_instance)

        if action_type == 'to_review':
            order_review_instance.for_review = True

        if action_type == 'approve':
            order_review_instance.for_review = False
            order_review_instance.is_approved = True

        order_review_instance.save()

        context = self.get_context_data()

        return render(request, self.template_table_name, context=context)
