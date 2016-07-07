# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileSys',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('parentid', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=20)),
                ('createdate', models.DateTimeField(blank=True)),
                ('creator', models.CharField(max_length=200)),
                ('filename', models.CharField(max_length=200, blank=True)),
                ('foldername', models.CharField(max_length=200, blank=True)),
                ('path', models.CharField(max_length=2000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShortLink',
            fields=[
                ('id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('link', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=200)),
                ('authID', models.CharField(max_length=50)),
                ('authTime', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userName', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
    ]
