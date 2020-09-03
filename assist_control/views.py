import json
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import (
    RegisterForm
)
from django.contrib.auth.models import User
from .models import (
    Assistant, Service, AssistantService
)

# Create your views here.

def register_assistance(request):
    dates = [
        {
            'id': s.id,
            'date': datetime.strftime(datetime.combine(s.day, s.hour), '%Y-%m-%d %H:%M')
        } for s in Service.objects.filter(state='Y')
    ]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            next = True
            message = ''

            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('username')
            last_name = form.cleaned_data.get('username')
            phone = form.cleaned_data.get('phone')
            date_id = form.cleaned_data.get('date_id')

            service = Service.objects.get(id=date_id)

            if AssistantService.objects.filter(
                assistant_id=username, service_id=date_id
            ).exists():
                next = False
                message = 'Ya se encuentra registrado en el horario escogido.'

            if next:
                if not AssistantService.objects.filter(service_id=date_id).count() < service.max_attendees:
                    next = False
                    message = '¡Lo sentimos! Ya no hay cupo, intenta en otro horario.'

            if next:
                try:
                    user = User.objects.get(username=username)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                except User.DoesNotExist:
                    user = User(
                        username=username, first_name=first_name, last_name=last_name
                    )
                    user.save()

                try:
                    assistant = Assistant.objects.get(id=username)
                    assistant.first_name = user.first_name
                    assistant.last_name = user.last_name
                    assistant.phone = phone
                    assistant.save()
                except Assistant.DoesNotExist:
                    assistant = Assistant(
                        user=user, id=user.username, name=user.first_name,
                        last_name=user.last_name, phone=phone
                    )
                    assistant.save()

                assistant_service = AssistantService(
                    assistant = assistant, service=service, attended='N'
                )
                assistant_service.save()

                message = 'Registro realizado con éxito.'

            return render(request, 'register/register.html', {
                'message': message,
                'dates': dates
            })
    else:
        return render(request, 'register/register.html', {
            'dates': dates
        })
