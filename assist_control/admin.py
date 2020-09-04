from django.contrib import admin
from .models import Service, AssistantService

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


@admin.register(AssistantService)
class AssistantServiceAdmin(admin.ModelAdmin):
    list_display = (
        'assistant_id',
        'get_assistan_name',
        'get_day_service',
        'get_hour_service',
        'attended'
    )
    search_fields = ('assistant_id', 'get_assistan_name',)

    def get_assistan_name(self, obj):
        return obj.assistant.name

    def get_day_service(self, obj):
        return obj.service.day

    def get_hour_service(self, obj):
        return obj.service.hour
