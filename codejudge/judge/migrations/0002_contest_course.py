# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='course',
            field=models.ForeignKey(default=1, to='judge.Course'),
            preserve_default=False,
        ),
    ]
