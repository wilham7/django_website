# Generated by Django 3.0.3 on 2020-03-02 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0005_auto_20200303_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawings',
            name='drawing_title1',
            field=models.CharField(default='Architectural Services', max_length=200),
        ),
        migrations.AlterField(
            model_name='drawings',
            name='drawing_title3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
