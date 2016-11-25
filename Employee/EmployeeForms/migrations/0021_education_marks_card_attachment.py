# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-24 04:49
from __future__ import unicode_literals

import EmployeeForms.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeForms', '0020_auto_20161124_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='marks_card_attachment',
            field=models.FileField(blank=True, null=True, upload_to=EmployeeForms.models.content_file_name, verbose_name='Marks card Attachment'),
        ),
    ]
