# Generated by Django 3.0.3 on 2020-03-02 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0007_auto_20200303_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissions',
            options={'verbose_name_plural': 'Drawings'},
        ),
        migrations.AddField(
            model_name='submissions',
            name='req_drawings',
            field=models.ManyToManyField(to='drawingregister.Drawings'),
        ),
    ]
