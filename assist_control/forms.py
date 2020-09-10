# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Assistant
from django.forms import ModelForm

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    date_id = forms.IntegerField(required=True)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'age')


class CompleteAssistan(ModelForm):
    SYMPTOMS = (
        ('f', 'Fiebre'),
        ('t', 'Tos'),
        ('c', 'Cefalea'),
        ('dg', 'Dolor de Garganta'),
        ('mg', 'Malestar General'),
        ('dr', 'Dificultad Respiratoria'),
        ('a', 'Adinamia'),
        ('sn', 'Secreciones Nasales'),
        ('d', 'Diarrea'),
    )

    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    temperature = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    symptoms = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'list-group list-group-flush'}),
        choices=SYMPTOMS,
    )
    close_person = forms.BooleanField(required=False)
    washed = forms.BooleanField(required=False)
    agree = forms.BooleanField(required=False)
    was_returned = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(CompleteAssistan, self).__init__(*args, **kwargs)
        self.fields['id'].label = "Número de Identificación"
        self.fields['name'].label = "Nombre(s)"
        self.fields['last_name'].label = "Apellidos"
        self.fields['age'].label = "Edad"
        self.fields['phone'].label = "Teléfono"
        self.fields['address'].label = "Dirección"
        self.fields['temperature'].label = "Temperatura"
        self.fields['symptoms'].label = "¿Ha presentado alguno de estos síntomas en las últimas 24 horas?"
        self.fields['close_person'].label = "¿Ha estado en contacto con alguien que presente los anteriores sintomas en las últimas 24 horas?"
        self.fields['washed'].label = "¿Realizó el lavado o desinfección de las manos antes de ingresar a las instalaciones?"
        self.fields['agree'].label = "¿Está de acuerdo en cumplir a cabalidad con todas las recomendaciones y los procedimientos que la iglesia ha adoptado para la preservación de su salud?"
        self.fields['was_returned'].label = "¿Se le niega el ingreso a las instalaciones y se recomienda que regrese a casa?"

    class Meta:
        model = Assistant
        fields = ('id', 'name', 'last_name', 'age', 'phone', 'address')


class EditAssistan(ModelForm):
    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(EditAssistan, self).__init__(*args, **kwargs)
        self.fields['id'].label = "Número de Identificación"
        self.fields['name'].label = "Nombre(s)"
        self.fields['last_name'].label = "Apellidos"
        self.fields['phone'].label = "Teléfono"
        self.fields['age'].label = "Edad"
        self.fields['address'].label = "Dirección"

    class Meta:
        model = Assistant
        fields = ('id', 'name', 'last_name', 'age', 'phone', 'address')


class RegisterServant(forms.Form):
    SYMPTOMS = (
        ('f', 'Fiebre'),
        ('t', 'Tos'),
        ('c', 'Cefalea'),
        ('dg', 'Dolor de Garganta'),
        ('mg', 'Malestar General'),
        ('dr', 'Dificultad Respiratoria'),
        ('a', 'Adinamia'),
        ('sn', 'Secreciones Nasales'),
        ('d', 'Diarrea'),
    )

    id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    temperature = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    symptoms = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'list-group list-group-flush'}),
        choices=SYMPTOMS,
    )
    close_person = forms.BooleanField(required=False)
    washed = forms.BooleanField(required=False)
    agree = forms.BooleanField(required=False)
    dates = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'list-group list-group-flush'}),
        choices=(),
    )

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('dates_tuples')
        super(RegisterServant, self).__init__(*args, **kwargs)
        self.fields['id'].label = "Número de Identificación"
        self.fields['name'].label = "Nombre(s)"
        self.fields['last_name'].label = "Apellidos"
        self.fields['age'].label = "Edad"
        self.fields['phone'].label = "Teléfono"
        self.fields['address'].label = "Dirección"
        self.fields['temperature'].label = "Temperatura"
        self.fields['symptoms'].label = "¿Ha presentado alguno de estos síntomas en las últimas 24 horas?"
        self.fields['close_person'].label = "¿Ha estado en contacto con alguien que presente los anteriores sintomas en las últimas 24 horas?"
        self.fields['washed'].label = "¿Realizó el lavado o desinfección de las manos antes de ingresar a las instalaciones?"
        self.fields['agree'].label = "¿Está de acuerdo en cumplir a cabalidad con todas las recomendaciones y los procedimientos que la iglesia ha adoptado para la preservación de su salud?"
        self.fields["dates"].choices = choices

    class Meta:
        model = Assistant
        fields = ('id', 'name', 'last_name', 'age', 'phone', 'address')
