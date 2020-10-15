# Generated by Django 3.1.2 on 2020-10-13 18:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0020_auto_20201013_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fencingmodule',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 13, 13, 47, 27, 734789)),
        ),
        migrations.AlterField(
            model_name='trackerchip',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 13, 13, 47, 27, 734789)),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('orig', 'dest'), name='one_route'),
        ),
    ]