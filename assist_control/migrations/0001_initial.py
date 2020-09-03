# Generated by Django 3.1.1 on 2020-09-03 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('hour', models.TimeField()),
                ('max_attendees', models.IntegerField()),
                ('state', models.CharField(default='Y', max_length=1, null=True)),
                ('created_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssistantService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.CharField(default='N', max_length=1, null=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_control.assistant')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assist_control.service')),
            ],
        ),
    ]