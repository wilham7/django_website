# Generated by Django 3.0.3 on 2020-03-03 01:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20200303_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 3, 12, 20, 53, 18232), verbose_name='date published'),
        ),
    ]
