# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-08 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_problem_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='language',
            field=models.CharField(default=b'C', max_length=30),
        ),
    ]
