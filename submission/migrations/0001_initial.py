# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-03 12:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import util.shortcuts


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('util', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(db_index=True, default=util.shortcuts.rand_str, max_length=32, primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('judge_start_time', models.BigIntegerField(blank=True, null=True)),
                ('judge_end_time', models.BigIntegerField(blank=True, null=True)),
                ('local_problem_id', models.IntegerField(db_index=True)),
                ('public', models.BooleanField(default=False)),
                ('remote_oj_run_id', models.CharField(blank=True, max_length=50, null=True)),
                ('remote_oj_submit_id', models.CharField(default='crazyX', max_length=50)),
                ('remote_oj_submit_pwd', models.CharField(default='x970307jw', max_length=50)),
                ('remote_oj_problem_id', models.CharField(max_length=50)),
                ('language', models.IntegerField()),
                ('code', models.TextField()),
                ('result', models.IntegerField(default=0)),
                ('info', models.TextField(blank=True, null=True)),
                ('remote_oj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='util.OJ')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'submission',
            },
        ),
    ]
