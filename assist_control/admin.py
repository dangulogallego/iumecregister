from django.contrib import admin
from .models import Service, AssistantService
from django.http import HttpResponse
import csv
from datetime import datetime
from .actions import export_as_xls

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
        'get_date_attended',
        'get_hour_attended',
        'get_full_name',
        'get_assistan_id',
        'temperature',
        'get_fever',
        'get_cough',
        'get_headache',
        'get_sore_throat',
        'get_general_discomfort',
        'get_respiratory_difficulty',
        'get_adinamia',
        'get_nasal_secretions',
        'get_diarrhea',
        'get_close_person',
        'get_washed'
    )

    actions = [export_as_xls]

    search_fields = ('assistant_id', 'get_assistan_name',)

    def get_date_attended(self, obj):
        return datetime.strftime(obj.attended_date, '%Y-%m-%d') if obj.attended_date else None

    def get_hour_attended(self, obj):
        return datetime.strftime(obj.attended_date, '%I:%M %p') if obj.attended_date else None

    def get_full_name(self, obj):
        return obj.assistant.name + ' ' + obj.assistant.last_name

    def get_assistan_id(self, obj):
        return obj.assistant.id

    def get_fever(self, obj):
        return 'X' if obj.fever == 'Y' else ''

    def get_cough(self, obj):
        return 'X' if obj.cough == 'Y' else ''

    def get_headache(self, obj):
        return 'X' if obj.headache == 'Y' else ''

    def get_sore_throat(self, obj):
        return 'X' if obj.sore_throat == 'Y' else ''

    def get_general_discomfort(self, obj):
        return 'X' if obj.general_discomfort == 'Y' else ''

    def get_respiratory_difficulty(self, obj):
        return 'X' if obj.respiratory_difficulty == 'Y' else ''

    def get_adinamia(self, obj):
        return 'X' if obj.adinamia == 'Y' else ''

    def get_nasal_secretions(self, obj):
        return 'X' if obj.nasal_secretions == 'Y' else ''

    def get_diarrhea(self, obj):
        return 'X' if obj.diarrhea == 'Y' else ''

    def get_close_person(self, obj):
        return 'Si' if obj.diarrhea == 'Y' else 'No'

    def get_washed(self, obj):
        return 'Si' if obj.diarrhea == 'Y' else 'No'
