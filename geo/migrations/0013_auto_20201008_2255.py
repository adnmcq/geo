# Generated by Django 3.1.2 on 2020-10-09 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0012_auto_20201008_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 8, 22, 55, 13, 131595)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 8, 22, 55, 13, 132587)),
        ),
    ]