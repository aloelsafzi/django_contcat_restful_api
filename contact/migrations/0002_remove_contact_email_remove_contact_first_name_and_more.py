# Generated by Django 5.1.5 on 2025-01-21 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='last_name',
        ),
        migrations.AddField(
            model_name='contact',
            name='first_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='seconds_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='username',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
