# Generated by Django 3.0.3 on 2020-04-01 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_auto_20200401_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 12, 34, 55, 90952), verbose_name='date published'),
        ),
    ]