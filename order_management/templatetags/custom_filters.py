from django import template

register = template.Library()


@register.filter
def format_phone_number(value):
    value = str(value)
    if len(value) > 7:
        return f"{value[:3]}-{value[3:6]}-{value[6:]}"
    return value
