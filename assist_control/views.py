import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import (
    RegisterForm, CompleteAssistan, EditAssistan
)
from django.contrib.auth.models import User
from .models import (
    Assistant, Service, AssistantService
)
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    return redirect('register_assistance')


def register_assistance(request):
    dates = [
        {
            'id': s.id,
            'date': datetime.strftime(datetime.combine(s.day, s.hour), '%Y-%m-%d %H:%M')
        } for s in Service.objects.filter(state='Y')
    ]
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        message = ''
        success = True
        if form.is_valid():
            next = True

            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            date_id = form.cleaned_data.get('date_id')

            service = Service.objects.get(id=date_id)
            date_service = datetime.strftime(datetime.combine(service.day, service.hour), '%A, %d. %B %I:%M%p')

            if AssistantService.objects.filter(
                assistant_id=username, service_id=date_id
            ).exists():
                next = False
                message = '¡Lo sentimos! Ya se encuentra registrado para el día (' + date_service + ')'
                success = False

            if next:
                if not AssistantService.objects.filter(service_id=date_id).count() < service.max_attendees:
                    next = False
                    message = '¡Lo sentimos! Ya no hay cupo para el día (' + date_service + '), por favor intenta en otro horario.'
                    success = False

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

                message = 'Registro realizado con éxito para el día (' + date_service + ')'
                success = True

            return render(request, 'register/register.html', {
                'message': message,
                'dates': dates,
                'success': success
            })
        else:
            message = 'Ha ocurrido un error realizando en el registro, por favor revise toda la información e intente nuevamente.'
            success = False
            return render(request, 'register/register.html', {
                'message': message,
                'dates': dates,
                'success': success
            })
    else:
        return render(request, 'register/register.html', {
            'dates': dates
        })


def services_list(request):
    dates = [
        {
            'id': s.id,
            'day': datetime.strftime(s.day, '%Y-%m-%d'),
            'hour': s.hour,
            'max_attendees': s.max_attendees,
            'inscribed': AssistantService.objects.filter(service_id=s.id).count(),
            'attendees': AssistantService.objects.filter(attended='Y', service_id=s.id).count()
        } for s in Service.objects.filter(state='Y')
    ]

    return render(request, 'services/list.html', {
        'services': dates
    })


def service_assistants(request, service_pk):
    filter = Q()
    page = request.GET.get('page', 1)
    data_filter = request.GET.get('filter')

    if request.GET and data_filter:
        filter = Q(assistant__id__icontains=data_filter) | Q(assistant__name__icontains=data_filter) | Q(assistant__last_name__icontains=data_filter)

    qs_assistants = AssistantService.objects.filter(filter, service=service_pk)
    paginator = Paginator(qs_assistants, 7)

    try:
        assistants_list = paginator.page(page)
    except PageNotAnInteger:
        assistants_list = paginator.page(1)
    except EmptyPage:
        assistants_list = paginator.page(paginator.num_pages)

    assistants = [
        {
            'id': a.assistant_id,
            'name': a.assistant.name,
            'last_name': a.assistant.last_name,
            'day': datetime.strftime(a.service.day, '%Y-%m-%d'),
            'hour': a.service.hour,
            'service_id': a.service_id,
            'service_assistant_id': a.id,
            'attended': a.attended
        } for a in assistants_list
    ]

    return render(request, 'assistants/list.html', {
        'assistants': assistants,
        'service_id': service_pk,
        'assistants_paginator': assistants_list,
        'filter': data_filter
    })


def complete_assistant(request, assistant_service_pk):
    assistant_service = AssistantService.objects.get(id=assistant_service_pk)
    assistant = Assistant.objects.get(id=assistant_service.assistant_id)
    if request.method == 'POST':
        form = CompleteAssistan(request.POST, instance=assistant)
        if form.is_valid():
            assistant_service.attended = 'Y'
            assistant_service.attended_date = timezone.now()
            symptoms = form.cleaned_data.get('symptoms', [])
            assistant_service.fever = 'Y' if 'f' in symptoms else 'N'
            assistant_service.cough = 'Y' if 't' in symptoms else 'N'
            assistant_service.headache = 'Y' if 'c' in symptoms else 'N'
            assistant_service.sore_throat = 'Y' if 'dg' in symptoms else 'N'
            assistant_service.general_discomfort = 'Y' if 'mg' in symptoms else 'N'
            assistant_service.respiratory_difficulty = 'Y' if 'dr' in symptoms else 'N'
            assistant_service.adinamia = 'Y' if 'a' in symptoms else 'N'
            assistant_service.nasal_secretions = 'Y' if 'sn' in symptoms else 'N'
            assistant_service.diarrhea = 'Y' if 'd' in symptoms else 'N'
            assistant_service.close_person = 'Y' if form.cleaned_data.get('close_person', False) else 'N'
            assistant_service.washed = 'Y' if form.cleaned_data.get('washed', False) else 'N'
            assistant_service.temperature = form.cleaned_data.get('temperature', 0)
            assistant_service.save()
            form.save()

            return redirect('service_assistants', service_pk=assistant_service.service_id)
    else:
        form = CompleteAssistan(instance=assistant)

        return render(request, 'assistants/complete_assistant.html', {
            'form': form,
            'assistant': assistant,
            'assistant_service': assistant_service,
            'day': datetime.strftime(assistant_service.service.day, '%Y-%m-%d'),
            'hour': assistant_service.service.hour,
        })


def edit_assistant(request, assistant_service_pk):
    assistant_service = AssistantService.objects.get(id=assistant_service_pk)
    assistant = Assistant.objects.get(id=assistant_service.assistant_id)
    message = ''
    success = True

    if request.method == 'POST':
        form = EditAssistan(request.POST, instance=assistant)
        if form.is_valid():
            form.save()
            message = 'Se ha actualizado la información con éxito'
            success = True
    else:
        form = EditAssistan(instance=assistant)

    return render(request, 'assistants/edit.html', {
        'form': form,
        'assistant': assistant,
        'assistant_service': assistant_service,
        'message': message,
        'success': success
    })


def remove_non_attendees(request, service_pk):
    AssistantService.objects.filter(
        service_id=service_pk, attended='N'
    ).delete()

    return redirect('services_list')
