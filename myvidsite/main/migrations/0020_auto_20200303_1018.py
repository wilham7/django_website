# Generated by Django 3.0.3 on 2020-03-02 23:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20200228_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 3, 10, 18, 18, 287416), verbose_name='date published'),
        ),
    ]
