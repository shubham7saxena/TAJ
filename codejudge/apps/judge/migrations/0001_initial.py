# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contestName', models.CharField(unique=True, max_length=200)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=200)),
                ('extension', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('problemSetter', models.CharField(max_length=200)),
                ('problemTitle', models.CharField(max_length=200)),
                ('problemStatement', ckeditor.fields.RichTextField()),
                ('testInput', models.FileField(upload_to=b'testInput')),
                ('testOutput', models.FileField(upload_to=b'testOutput')),
                ('timeLimit', models.PositiveSmallIntegerField()),
                ('languagesAllowed', models.CommaSeparatedIntegerField(max_length=200)),
                ('inputFormat', ckeditor.fields.RichTextField()),
                ('outputFormat', ckeditor.fields.RichTextField()),
                ('constraints', ckeditor.fields.RichTextField()),
                ('sampleInput', ckeditor.fields.RichTextField()),
                ('sampleOutput', ckeditor.fields.RichTextField()),
                ('solvedBy', models.PositiveSmallIntegerField(default=0)),
                ('contest', models.ForeignKey(to='judge.Contest')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('solution', models.FileField(upload_to=b'solution')),
                ('attempts', models.PositiveSmallIntegerField()),
                ('time', models.DecimalField(max_digits=2, decimal_places=2)),
                ('status', models.PositiveSmallIntegerField()),
                ('contest', models.ForeignKey(to='judge.Contest')),
                ('hacker', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(to='judge.Language')),
                ('problem', models.ForeignKey(to='judge.Problem')),
            ],
        ),
    ]
