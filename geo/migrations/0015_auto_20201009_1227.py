# Generated by Django 3.1.2 on 2020-10-09 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0014_auto_20201008_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='markers',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 12, 27, 45, 776250)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 9, 12, 27, 45, 776250)),
        ),
    ]
