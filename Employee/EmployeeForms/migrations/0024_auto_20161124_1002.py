# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-24 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeForms', '0023_auto_20161124_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proof',
            name='dl',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Driving License'),
        ),
        migrations.AlterField(
            model_name='proof',
            name='passport',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Passport'),
        ),
    ]
