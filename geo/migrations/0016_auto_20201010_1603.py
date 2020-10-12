# Generated by Django 3.1.2 on 2020-10-10 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0015_auto_20201009_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='markers',
            new_name='endpoints',
        ),
        migrations.AddField(
            model_name='trip',
            name='fencing',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 10, 16, 2, 57, 433889)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 10, 16, 2, 57, 433889)),
        ),
    ]