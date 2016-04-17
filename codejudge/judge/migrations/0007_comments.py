# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0006_query'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commentText', models.TextField()),
                ('contest', models.ForeignKey(to='judge.Contest')),
                ('hacker', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(to='judge.Problem')),
            ],
        ),
    ]
