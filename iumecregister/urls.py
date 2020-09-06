"""iumecregister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from assist_control.views import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='index'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^assist/register/$', register_assistance, name='register_assistance'),
    url(r'^services/list/$', services_list, name='services_list'),
    url(r'^services/(?P<service_pk>[0-9]+)/assistants/$', service_assistants, name='service_assistants'),
    url(r'^services/assistants/(?P<assistant_service_pk>[0-9]+)/complete/$', complete_assistant, name='complete_assistant'),
    url(r'^services/(?P<service_pk>[0-9]+)/assistants/delete$', remove_non_attendees, name='remove_non_attendees'),
    url(r'^assistants/(?P<assistant_service_pk>[0-9]+)/edit/$', edit_assistant, name='edit_assistant'),
    url(r'^assistants/(?P<assistant_service_pk>[0-9]+)/remove/$', remove_non_attendee, name='remove_non_attendee'),
    url(r'^assist/servant/register/$', register_servant, name='register_servant'),
]
