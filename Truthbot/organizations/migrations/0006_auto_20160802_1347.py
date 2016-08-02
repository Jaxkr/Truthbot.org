# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20160802_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationwiki',
            name='organization',
        ),
        migrations.AddField(
            model_name='organization',
            name='wiki',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='organizations.OrganizationWiki'),
            preserve_default=False,
        ),
    ]
