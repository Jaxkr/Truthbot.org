# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-08 03:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_remove_article_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='summary',
        ),
    ]
