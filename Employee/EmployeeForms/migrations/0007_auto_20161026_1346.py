# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-26 13:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeForms', '0006_auto_20161025_0837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='institute',
            new_name='institution',
        ),
    ]
