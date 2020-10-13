# Generated by Django 3.1.2 on 2020-10-13 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0017_auto_20201011_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='checked_points',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 13, 9, 13, 42, 32746)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 13, 9, 13, 42, 33742)),
        ),
    ]