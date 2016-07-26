# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_postcomments_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomments',
            name='content',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
