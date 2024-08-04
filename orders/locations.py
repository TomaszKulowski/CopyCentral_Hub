from django.shortcuts import get_object_or_404
from geopy.geocoders import Nominatim


def get_coordinates(street, number, postal_code, city):
    geolocator = Nominatim(user_agent="CopyCentral_Hub")
    address = ''
    if street:
        address += f"{str(street).replace('ul.', '').replace('Ul.', '').replace('UL.', '').replace('uL.', '')} "
    if number:
        number = str(number).split('/')
        address += f'{number[0]}, '
    if postal_code:
        address += f'{postal_code} '
    if city:
        address += f'{city} ,'
    try:
        location = geolocator.geocode(address, exactly_one=True, timeout=5)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [0, 0]

    except Exception:
        return [0, 0]


def update_coordinates_from_address(instance, address):
    if address:
        coordinates = get_coordinates(
            address.street,
            address.number,
            address.postal_code,
            address.city,
        )
        if coordinates:
            instance.latitude = coordinates[0]
            instance.longitude = coordinates[1]


def update_order_coordinates(order):
    if not order._state.adding:
        old_order_instance = get_object_or_404(type(order), pk=order.pk)

        if old_order_instance.additional_address != order.additional_address:
            update_coordinates_from_address(order, order.additional_address)

        elif old_order_instance.customer != order.customer:
            if order.customer:
                address = type('Address', (object,), {
                    'street': order.customer.billing_street,
                    'number': order.customer.billing_number,
                    'postal_code': order.customer.billing_postal_code,
                    'city': order.customer.billing_city
                })()
                update_coordinates_from_address(order, address)

    if order._state.adding:
        if order.additional_address:
            update_coordinates_from_address(order, order.additional_address)
        elif order.customer:
            address = type('Address', (object,), {
                'street': order.customer.billing_street,
                'number': order.customer.billing_number,
                'postal_code': order.customer.billing_postal_code,
                'city': order.customer.billing_city
            })()
            update_coordinates_from_address(order, address)
