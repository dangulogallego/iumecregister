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
    phone = models.CharField(max_length=30, null=True)
    created_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.id

class Service(models.Model):
    day = models.DateField()
    hour = models.TimeField()
    max_attendees = models.IntegerField()
    state = models.CharField(max_length=1, null=True, default='Y')
    created_date = models.DateField(auto_now=True)

class AssistantService(models.Model):
    assistant = models.ForeignKey( 'Assistant', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    attended = models.CharField(max_length=1, null=True, default='N')
    created_date = models.DateField(auto_now=True)
