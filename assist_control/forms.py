# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    date_id = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone')
