# Generated by Django 3.0.3 on 2020-03-17 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0014_drawings_drawing_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissions',
            name='toBeSubmitted',
            field=models.ManyToManyField(blank=True, related_name='toBeSubmitted', to='drawingregister.Drawings'),
        ),
    ]
