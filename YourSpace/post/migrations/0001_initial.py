# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField(blank=True, max_length=400)),
                ('image', models.ImageField(blank=True, upload_to='posts/%Y/%m/%d')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('total_likes', models.IntegerField(default=0)),
                ('likes', models.ManyToManyField(related_name='liked_post', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField(blank=True, max_length=100)),
                ('post', models.ForeignKey(to='post.Post')),
            ],
        ),
    ]
