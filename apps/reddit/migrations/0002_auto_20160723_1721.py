# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-23 14:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reddit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='votes',
        ),
        migrations.AddField(
            model_name='thread',
            name='voters',
            field=models.ManyToManyField(related_name='voted_thread', to=settings.AUTH_USER_MODEL),
        ),
    ]
