# Generated by Django 3.0.3 on 2020-03-17 04:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20200317_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 17, 15, 24, 13, 889587), verbose_name='date published'),
        ),
    ]
