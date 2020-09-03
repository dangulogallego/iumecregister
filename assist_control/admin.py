from django.contrib import admin
from .models import Service

# Register your models here.

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'day',
        'hour',
        'max_attendees',
        'state'
    )
    search_fields = ('day',)
