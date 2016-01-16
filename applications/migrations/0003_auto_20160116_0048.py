# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 00:48
from __future__ import unicode_literals

import applications.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20160115_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='essay',
            field=models.CharField(default='', max_length=100000, validators=[applications.models.validate_essay_length], verbose_name='Candidate Essay'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='essay',
            field=models.CharField(default='', max_length=100000, validators=[applications.models.validate_essay_length], verbose_name='Trainee Essay'),
        ),
    ]
