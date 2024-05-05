import os
import subprocess

from datetime import datetime

from django.conf import settings
from django.utils.translation import activate, gettext_lazy as _
from mailmerge import MailMerge

from orders.models import StatusChoices, PriorityChoices, OrderTypeChoices, PaymentMethodChoices, Order


def map_choices_int_to_str(orders):
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


def docx_to_pdf(doc_path, dir):
    name, extension = os.path.splitext(doc_path)

    subprocess.call([
        '/usr/bin/soffice',
        '--headless',
        '--convert-to',
        'pdf',
        '--outdir',
        dir,
        doc_path,
    ])
    return name + '.pdf'


def get_report(order, employee_name, language):
    activate(language)
    report = _('report')

    template = "templates/orders/order_report_template.docx"
    document = MailMerge(template)
    intake_first_name = order.user_intake.user.first_name
    intake_last_name = order.user_intake.user.last_name

    services = []
    total_price_net = 0
    for index, service in enumerate(order.services.all(), 1):
        if service.price_net:
            total_price_net += service.price_net * service.quantity
            price_gross = f'{service.price_net * 1.23} zł'
            price_net = f'{service.price_net} zł'
        else:
            price_gross = None
            price_net = None

        services.append(
            {
                'num': str(index),
                'service': str(service.name),
                'qty': str(service.quantity),
                'price_net': price_net,
                'price_gross': price_gross,
            }
        )
    document.merge_rows('service', services)
    total_price_gross = total_price_net * 1.23
    if total_price_net:
        total_price_net = f'{total_price_net} zł'
        total_price_gross = f'{total_price_gross} zł'
    else:
        total_price_net = None
        total_price_gross = None

    if order.additional_address:
        address = str(order.additional_address)
    else:
        address = order.customer.get_address()

    if order.total_counter:
        total_counter = f'total: {order.total_counter} '
    else:
        total_counter = ''
    if order.mono_counter:
        mono_counter = f'mono: {order.mono_counter} '
    else:
        mono_counter = ''
    if order.color_counter:
        color_counter = f'color: {order.color_counter} '
    else:
        color_counter = ''

    fields = {
        'order_id': str(order.id),
        'intake_date': str(order.created_at.date()),
        'order_intake': f'{intake_first_name}.{intake_last_name[0]}',
        'customer': str(order.customer),
        'address': address,
        'additional_info': order.additional_info,
        'description': order.description,
        'tel': order.phone_number,
        'total_counter': total_counter,
        'mono_c': mono_counter,
        'color_c': color_counter,
        'payment_method': order.get_payment_method_display(),
        'priority': order.get_priority_display(),
        'current_date': str(datetime.now().strftime('%d-%m-%Y %H:%M')),
        'employee_sign': employee_name,
        'customer_sign': order.signer_name,
        'p_total_net': total_price_net,
        'p_total_gross': total_price_gross,
    }
    if order.device:
        fields['device'] = str(order.device)
        fields['serial_number'] = order.device.serial_number
    else:
        fields['device'] = order.device_name

    document.merge(**{field_name: str(value) for field_name, value in fields.items() if value})

    if order.order_type == 0:
        document.merge(x='X')
    if order.order_type == 1:
        document.merge(z='X')
    if order.order_type == 2:
        document.merge(c='X')
    if order.order_type == 3:
        document.merge(v='X')
    if order.order_type == 4:
        document.merge(b='X')
    if order.order_type == 5:
        document.merge(x='?')
    if order.order_type == 6:
        document.merge(z='?')
    if order.order_type == 7:
        document.merge(c='?')
    if order.order_type == 8:
        document.merge(v='?')
    if order.order_type == 9:
        document.merge(b='?')

    media_path = settings.MEDIA_ROOT
    current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    reports_dir = os.path.join(media_path, 'reports', str(order.id))
    os.makedirs(reports_dir, exist_ok=True)
    document_path = os.path.join(reports_dir, f'{report}_{order.id}_{current_datetime}.docx')
    document.write(document_path)
    report_path = docx_to_pdf(document_path, reports_dir)

    if os.path.exists(document_path):
        os.remove(document_path)

    return report_path
