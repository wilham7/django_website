# Generated by Django 3.0.3 on 2020-03-03 00:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20200303_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 3, 11, 24, 25, 268244), verbose_name='date published'),
        ),
    ]