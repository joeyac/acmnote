# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 01:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_problem_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='last_update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='最后更新时间'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
