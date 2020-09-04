from django.template import Library
import locale
import datetime
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

register = Library()


@register.filter(is_safe=True)
def dates(value):
    date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
    return date.strftime('%A, %d. %B %I:%M%p')


@register.filter(is_safe=True)
def parse_date(value):
    date = datetime.datetime.strptime(value, '%Y-%m-%d')
    return date.strftime('%A, %d. %B')


@register.filter(is_safe=True)
def parse_time(value):
    return value.strftime('%I:%M%p')


@register.filter(is_safe=True)
def subtract(value, arg):
    return value-arg


@register.filter(is_safe=True)
def parse_yes_not(value):
    return 'Si' if value == 'Y' else 'No'
