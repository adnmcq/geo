# Generated by Django 3.1.2 on 2020-10-12 03:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0016_auto_20201010_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 22, 9, 30, 893193)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 11, 22, 9, 30, 894189)),
        ),
        migrations.AlterField(
            model_name='trip',
            name='endpoints',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='trip',
            name='fencing',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='trip',
            name='route',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
