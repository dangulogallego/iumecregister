# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Assistant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    phone = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.id) +  ' - ' + str(self.name)

class Service(models.Model):
    BooleanChoises = (
        ('Y', 'Activo'),
        ('N', 'Inactivo')
    )
    day = models.DateField()
    hour = models.TimeField()
    max_attendees = models.IntegerField()
    state = models.CharField(max_length=1, null=True, default='Y', choices=BooleanChoises)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.day) +  ' - ' + str(self.hour)


class AssistantService(models.Model):
    BooleanChoises = (
        ('Y', 'Activo'),
        ('N', 'Inactivo')
    )
    assistant = models.ForeignKey( 'Assistant', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    attended = models.CharField(max_length=1, null=True, default='N')
    attended_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now=True)
    fever = models.CharField(max_length=1, default='N', null=True)
    cough = models.CharField(max_length=1, default='N', null=True)
    headache = models.CharField(max_length=1, default='N', null=True)
    sore_throat = models.CharField(max_length=1, default='N', null=True)
    general_discomfort = models.CharField(max_length=1, default='N', null=True)
    respiratory_difficulty = models.CharField(max_length=1, default='N', null=True)
    adinamia = models.CharField(max_length=1, default='N', null=True)
    nasal_secretions = models.CharField(max_length=1, default='N', null=True)
    diarrhea = models.CharField(max_length=1, default='N', null=True)
    temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    close_person = models.CharField(max_length=1, default='N', null=True)
    washed = models.CharField(max_length=1, default='N', null=True)
    agree = models.CharField(max_length=1, default='N', null=True)
    is_servant = models.CharField(max_length=1, null=True, default='N', choices=BooleanChoises)
