# Generated by Django 3.0.3 on 2020-03-25 04:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_auto_20200325_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 15, 6, 29, 844617), verbose_name='date published'),
        ),
    ]
