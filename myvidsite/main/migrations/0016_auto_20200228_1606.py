# Generated by Django 3.0.3 on 2020-02-28 05:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200221_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 28, 16, 6, 25, 838327), verbose_name='date published'),
        ),
    ]