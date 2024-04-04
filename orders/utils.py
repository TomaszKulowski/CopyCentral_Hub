from orders.models import StatusChoices, PriorityChoices, OrderTypeChoices, PaymentMethodChoices


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
