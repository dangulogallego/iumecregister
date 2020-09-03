from django.template import Library
import locale
import datetime
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

register = Library()


@register.filter(is_safe=True)
def dates(value):
    date = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
    return date.strftime('%A, %B %d %Y %H:%M %p')
