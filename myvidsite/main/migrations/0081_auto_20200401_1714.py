# Generated by Django 3.0.3 on 2020-04-01 06:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20200401_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 17, 14, 48, 231471), verbose_name='date published'),
        ),
    ]