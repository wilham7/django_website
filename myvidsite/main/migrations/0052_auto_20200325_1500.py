# Generated by Django 3.0.3 on 2020-03-25 04:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_auto_20200324_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 15, 0, 24, 789927), verbose_name='date published'),
        ),
    ]
