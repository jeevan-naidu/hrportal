# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-02 04:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeForms', '0032_auto_20161201_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='qualification',
            field=models.CharField(choices=[('SSC', 'Senior Secondary'), ('HSC', 'Higher Secondary'), ('GRAD', 'Graduate'), ('PG', 'Post Graduate')], max_length=5, unique=True, verbose_name='Qualification'),
        ),
    ]
