# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-15 22:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('userdashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='users',
            managers=[
                ('create', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='user_level',
            field=models.IntegerField(default=9),
            preserve_default=False,
        ),
    ]
