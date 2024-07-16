import requests

from django.db.models import F

from .models import Notification, NotificationSettings
from orders.models import Order


def send_sms_message(server, auth_token, phone_number, message):
    payload = {
        'token': auth_token,
        'phoneno': f'+{phone_number}',
        'message': message,
    }
    return requests.post(server, data=payload)


def get_executors_orders():
    orders = Order.objects.exclude(status__in=[2, 3, 4, 5]).filter(
        executor__isnull=False,
    ).exclude(
        last_notification_executor=F('executor')
    ).select_related('executor').order_by('executor')

    grouped_orders = {}

    for order in orders:
        executor_id = order.executor.id

        if executor_id not in grouped_orders:
            grouped_orders[executor_id] = {
                'executor': order.executor,
                'executor_orders': []
            }

        grouped_orders[executor_id]['executor_orders'].append(order)

    return grouped_orders


def create_executor_notification():
    settings = NotificationSettings.objects.filter(notification_type=0).first()
    if settings:
        for executor_id, orders in get_executors_orders().items():

            order_numbers = ''
            for index, order in enumerate(orders['executor_orders'], 1):
                order.last_notification_executor = orders['executor']
                order.save()
                if index == len(orders['executor_orders']):
                    order_numbers += f'{str(order.id)}'
                else:
                    order_numbers += f'{str(order.id)}, '
            message = settings.message_template.replace('$orders_ids', order_numbers)

            Notification(
                settings=settings,
                receiver_name=str(orders['executor']),
                phone_number=orders['executor'].phone_number,
                message=message
            ).save()
    return True


def schedule_executor_notification():
    if create_executor_notification():
        unsent_notifications = Notification.objects.filter(sent=False)

        for notification in unsent_notifications:
            try:
                response = send_sms_message(
                    server=notification.settings.server,
                    auth_token=notification.settings.auth_token,
                    phone_number=f'{notification.phone_number}',
                    message=notification.message,
                )
                if response.json().get('success'):
                    notification.sent = True
                    notification.save()
            except Exception as error:
                print('send notification error: ', error)
                continue


def mark_orders_as_sent():
    Order.objects.all().update(last_notification_executor=F('executor'))

