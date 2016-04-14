# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0005_auto_20160413_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query_from', models.EmailField(max_length=255)),
                ('query_text', models.CharField(max_length=500)),
            ],
        ),
    ]
