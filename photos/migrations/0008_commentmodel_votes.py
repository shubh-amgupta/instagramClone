# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0007_postmodel_ifdirty'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]