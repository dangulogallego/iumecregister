import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import (
    RegisterForm, CompleteAssistan, EditAssistan, RegisterServant
)
from django.contrib.auth.models import User
from .models import (
    Assistant, Service, AssistantService
)
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('index')


def home(request):
    if request.user.is_authenticated:
        return redirect('services_list')
    else:
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
            age = form.cleaned_data.get('age')
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
                # Se excluye a los servidores y los que fueron devueltos de los cupos disponibles.
                if not AssistantService.objects.filter(service_id=date_id, is_servant='N', was_returned='N').count() < service.max_attendees:
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
                    assistant.age = age
                    assistant.save()
                except Assistant.DoesNotExist:
                    assistant = Assistant(
                        user=user, id=user.username, name=user.first_name,
                        last_name=user.last_name, phone=phone, age=age
                    )
                    assistant.save()

                assistant_service = AssistantService(
                    assistant=assistant, service=service, attended='N', is_servant='N', was_returned='N'
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
    if request.user.is_authenticated:
        dates = [
            {
                'id': s.id,
                'day': datetime.strftime(s.day, '%Y-%m-%d'),
                'hour': s.hour,
                'max_attendees': s.max_attendees,
                'inscribed': AssistantService.objects.filter(service_id=s.id, is_servant='N', was_returned='N').count(),  # Quedan excluídos los servidores y los que se devuelven
                'attendees': AssistantService.objects.filter(attended='Y', service_id=s.id, is_servant='N', was_returned='N').count(),
                'diference_to_delete': AssistantService.objects.filter(service_id=s.id, is_servant='N', was_returned='N').count() - AssistantService.objects.filter(attended='Y', service_id=s.id, is_servant='N', was_returned='N').count(),
                'servants': AssistantService.objects.filter(service_id=s.id, attended='Y', is_servant='Y', was_returned='N').count(),
                'returned': AssistantService.objects.filter(service_id=s.id, attended='N', was_returned='Y').count()
            } for s in Service.objects.filter(state='Y')
        ]

        return render(request, 'services/list.html', {
            'services': dates
        })
    else:
        return redirect('login')


def service_assistants(request, service_pk):
    if request.user.is_authenticated:
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
                'attended': a.attended,
                'is_servant': a.is_servant,
                'was_returned': a.was_returned
            } for a in assistants_list
        ]

        return render(request, 'assistants/list.html', {
            'assistants': assistants,
            'service_id': service_pk,
            'assistants_paginator': assistants_list,
            'filter': data_filter
        })
    else:
        return redirect('login')


def complete_assistant(request, assistant_service_pk):
    if request.user.is_authenticated:
        assistant_service = AssistantService.objects.get(id=assistant_service_pk)
        assistant = Assistant.objects.get(id=assistant_service.assistant_id)
        if request.method == 'POST':
            form = CompleteAssistan(request.POST, instance=assistant)
            if form.is_valid():

                was_returned = form.cleaned_data.get('was_returned', False)
                if was_returned:
                    assistant_service.was_returned = 'Y'
                    assistant_service.attended = 'N'
                else:
                    assistant_service.was_returned = 'N'
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
                assistant_service.agree = 'Y' if form.cleaned_data.get('agree', False) else 'N'
                assistant_service.temperature = form.cleaned_data.get('temperature', 0)
                assistant_service.save()
                form.save()

                return redirect('service_assistants', service_pk=assistant_service.service_id)
        else:
            symptoms = []
            if assistant_service.fever == 'Y':
                symptoms.append('f')
            if assistant_service.cough == 'Y':
                symptoms.append('t')
            if assistant_service.headache == 'Y':
                symptoms.append('c')
            if assistant_service.sore_throat == 'Y':
                symptoms.append('dg')
            if assistant_service.general_discomfort == 'Y':
                symptoms.append('mg')
            if assistant_service.respiratory_difficulty == 'Y':
                symptoms.append('dr')
            if assistant_service.adinamia == 'Y':
                symptoms.append('a')
            if assistant_service.nasal_secretions == 'Y':
                symptoms.append('sn')
            if assistant_service.diarrhea == 'Y':
                symptoms.append('d')

            form = CompleteAssistan(instance=assistant, initial={
                'washed': True if assistant_service.washed == 'Y' else False,
                'close_person': True if assistant_service.close_person == 'Y' else False,
                'agree': True if assistant_service.agree == 'Y' else False,
                'temperature': assistant_service.temperature if assistant_service.temperature else None,
                'symptoms': symptoms,
                'was_returned': True if assistant_service.was_returned == 'Y' else False
            })

            return render(request, 'assistants/complete_assistant.html', {
                'form': form,
                'assistant': assistant,
                'assistant_service': assistant_service,
                'day': datetime.strftime(assistant_service.service.day, '%Y-%m-%d'),
                'hour': assistant_service.service.hour,
            })
    else:
        return redirect('login')


def edit_assistant(request, assistant_service_pk):
    if request.user.is_authenticated:
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
    else:
        return redirect('login')


def remove_non_attendees(request, service_pk):
    if request.user.is_authenticated:
        # Eliminar los asistentes que no llegaron y que no fueron devueltos.
        AssistantService.objects.filter(
            service_id=service_pk, attended='N', was_returned='N'
        ).delete()

        return redirect('services_list')
    else:
        return redirect('login')


def remove_non_attendee(request, assistant_service_pk):
    if request.user.is_authenticated:
        assistant_service = AssistantService.objects.get(
            id=assistant_service_pk
        )
        service_id = assistant_service.service_id
        assistant_service.delete()
        return redirect('service_assistants', service_pk=service_id)
    else:
        return redirect('login')


def register_servant(request):
    dates = [
        {
            'id': s.id,
            'date': datetime.strptime(datetime.strftime(datetime.combine(s.day, s.hour), '%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M').strftime('%A, %d. %B %I:%M%p')
        } for s in Service.objects.filter(state='Y')
    ]

    dates_tuples = []
    for s in dates:
        dates_tuples.append((s['id'], s['date']),)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterServant(request.POST, dates_tuples=dates_tuples)
            message = ''
            success = True
            if form.is_valid():
                next = True

                id = form.cleaned_data.get('id')
                name = form.cleaned_data.get('name')
                last_name = form.cleaned_data.get('last_name')
                age = form.cleaned_data.get('age')
                phone = form.cleaned_data.get('phone')
                address = form.cleaned_data.get('address')
                temperature = form.cleaned_data.get('temperature')
                symptoms = form.cleaned_data.get('symptoms')
                close_person = form.cleaned_data.get('close_person')
                washed = form.cleaned_data.get('washed')
                agree = form.cleaned_data.get('agree')
                dates = form.cleaned_data.get('dates')

                if dates:
                    dates = [int(s) for s in dates]
                else:
                    dates = []

                assistant_services = AssistantService.objects.filter(
                    assistant_id=id, service_id__in=dates)

                if len(assistant_services) > 0:
                    dates_str = ''
                    for ase in assistant_services:
                        dates_str += datetime.strftime(datetime.combine(ase.service.day, ase.service.hour), '%A, %d. %B %I:%M%p') + ' '
                    message = '¡Lo sentimos! Ya se encuentra registrado para el(los) día(s) (' + dates_str + ') '
                    next = False
                    success = False

                if next:
                    try:
                        user = User.objects.get(username=id)
                        user.first_name = name
                        user.last_name = last_name
                        user.save()
                    except User.DoesNotExist:
                        user = User(
                            username=id, first_name=name, last_name=last_name
                        )
                        user.save()

                    try:
                        assistant = Assistant.objects.get(id=id)
                        assistant.first_name = user.first_name
                        assistant.last_name = user.last_name
                        assistant.phone = phone
                        assistant.age = age
                        assistant.address = address
                        assistant.save()
                    except Assistant.DoesNotExist:
                        assistant = Assistant(
                            user=user, id=user.username, name=user.first_name,
                            last_name=user.last_name, phone=phone, age=age, address=address
                        )
                        assistant.save()

                    services = Service.objects.filter(id__in=dates)
                    assistant_services = []

                    fever = 'Y' if 'f' in symptoms else 'N'
                    cough = 'Y' if 't' in symptoms else 'N'
                    headache = 'Y' if 'c' in symptoms else 'N'
                    sore_throat = 'Y' if 'dg' in symptoms else 'N'
                    general_discomfort = 'Y' if 'mg' in symptoms else 'N'
                    respiratory_difficulty = 'Y' if 'dr' in symptoms else 'N'
                    adinamia = 'Y' if 'a' in symptoms else 'N'
                    nasal_secretions = 'Y' if 'sn' in symptoms else 'N'
                    diarrhea = 'Y' if 'd' in symptoms else 'N'
                    close_person = 'Y' if form.cleaned_data.get('close_person', False) else 'N'
                    washed = 'Y' if form.cleaned_data.get('washed', False) else 'N'
                    agree = 'Y' if form.cleaned_data.get('agree', False) else 'N'
                    temperature = form.cleaned_data.get('temperature', 0)

                    for s in services:
                        assistant_services.append(
                            AssistantService(
                                assistant=assistant, service=s, attended='Y', attended_date=timezone.now(),
                                fever=fever, cough=cough, headache=headache, sore_throat=sore_throat,
                                general_discomfort=general_discomfort, respiratory_difficulty=respiratory_difficulty,
                                adinamia=adinamia, nasal_secretions=nasal_secretions, diarrhea=diarrhea,
                                temperature=temperature, close_person=close_person, washed=washed, agree=agree,
                                created_date=timezone.now(), is_servant='Y', was_returned='N'
                            )
                        )

                    if len(assistant_services) > 0:
                        AssistantService.objects.bulk_create(assistant_services)

                    message = 'Registro realizado con éxito '
                    success = True

                return render(request, 'register/servant-register.html', {
                    'message': message,
                    'dates': dates,
                    'success': success
                })

            else:
                message = 'Ha ocurrido un error realizando en el registro, por favor revise toda la información e intente nuevamente.'
                success = False
                return render(request, 'register/servant-register.html', {
                    'message': message,
                    'dates': dates,
                    'success': success
                })
        else:
            form = RegisterServant(dates_tuples=dates_tuples)
            return render(request, 'register/servant-register.html', {
                'form': form,
                'dates': dates
            })
    else:
        return redirect('login')
