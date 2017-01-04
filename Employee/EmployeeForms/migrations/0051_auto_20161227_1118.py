# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-27 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeForms', '0050_auto_20161227_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3, verbose_name='Blood Group'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='emergency_phone1',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Emergency Contact Number1'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='emergency_phone2',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Emergency Contact Number2'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='land_phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Landline Number'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_phone',
            field=models.CharField(max_length=10, unique=True, verbose_name='Mobile Phone'),
        ),
    ]
