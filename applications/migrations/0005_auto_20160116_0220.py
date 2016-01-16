# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 02:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0004_auto_20160116_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdevuser',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.Candidate'),
        ),
        migrations.AlterField(
            model_name='appdevuser',
            name='trainee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.Trainee'),
        ),
    ]
