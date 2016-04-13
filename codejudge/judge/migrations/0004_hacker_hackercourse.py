# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0003_remove_course_hacker'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='hackerCourse',
            field=models.ManyToManyField(to='judge.Course'),
        ),
    ]
