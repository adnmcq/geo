# Generated by Django 2.1.4 on 2020-10-02 15:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0007_auto_20200926_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 2, 10, 24, 11, 343662)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 2, 10, 24, 11, 343662)),
        ),
    ]
