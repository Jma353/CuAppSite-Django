# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-15 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='resume_link',
            field=models.CharField(max_length=200, null=True, verbose_name='Resume Link'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='portfolio_link',
            field=models.CharField(default='', max_length=200, verbose_name='Portfolio Link'),
        ),
        migrations.AlterField(
            model_name='trainee',
            name='resume_link',
            field=models.CharField(max_length=200, null=True, verbose_name='Resume Link'),
        ),
    ]
