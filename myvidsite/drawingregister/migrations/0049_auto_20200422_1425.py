# Generated by Django 3.0.3 on 2020-04-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0048_auto_20200415_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawings',
            name='drawing_name',
            field=models.CharField(blank=True, default='', max_length=200, unique=True),
        ),
    ]
