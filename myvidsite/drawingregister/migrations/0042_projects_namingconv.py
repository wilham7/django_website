# Generated by Django 3.0.3 on 2020-04-01 04:49

from django.db import migrations
import drawingregister.models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0041_auto_20200401_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='namingConv',
            field=drawingregister.models.DataField(blank=True, default={}, max_length=9999),
        ),
    ]