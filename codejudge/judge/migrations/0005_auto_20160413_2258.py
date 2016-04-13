# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0004_hacker_hackercourse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hacker',
            old_name='hackerCourse',
            new_name='course',
        ),
    ]
