# Generated by Django 3.0.5 on 2020-10-08 00:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0009_auto_20201005_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='geo.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 19, 40, 0, 485837)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 19, 40, 0, 486859)),
        ),
    ]
