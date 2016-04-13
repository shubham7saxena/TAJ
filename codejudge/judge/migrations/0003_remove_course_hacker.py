# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_contest_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='hacker',
        ),
    ]
