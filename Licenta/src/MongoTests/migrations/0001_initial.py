# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('readState', models.BooleanField()),
                ('readPercentage', models.CharField(max_length=200)),
                ('readKeys', models.CharField(max_length=200)),
                ('readSize', models.CharField(max_length=200)),
                ('writeState', models.BooleanField()),
                ('writePercentage', models.CharField(max_length=200)),
                ('writeKeys', models.CharField(max_length=200)),
                ('writeSize', models.CharField(max_length=200)),
                ('updateState', models.BooleanField()),
                ('updatePercentage', models.CharField(max_length=200)),
                ('updateKeys', models.CharField(max_length=200)),
                ('updateSize', models.CharField(max_length=200)),
            ],
        ),
    ]
