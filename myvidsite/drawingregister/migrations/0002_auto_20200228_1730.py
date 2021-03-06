# Generated by Django 3.0.3 on 2020-02-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawings',
            name='discipline',
            field=models.CharField(default='Architectural', max_length=200),
        ),
        migrations.AddField(
            model_name='drawings',
            name='dwg_type',
            field=models.CharField(choices=[('2D Drawing', '2D Drawing'), ('2D Model', '2D Model'), ('3D Model', '3D Model'), ('Animation File', 'Animation File'), ('Calculation', 'Calculation'), ('Certificate', 'Certificate'), ('Clash Report', 'Clash Report'), ('Combined Model', 'Combined Model'), ('Correspondence', 'Correspondence'), ('Cost Plan', 'Cost Plan'), ('Database', 'Database'), ('Drawing', 'Drawing'), ('File Note', 'File Note'), ('Information Exchange File', 'Information Exchange File'), ('Material Sample', 'Material Sample'), ('Matrix', 'Matrix'), ('Meeting Minutes', 'Meeting Minutes'), ('Model Rendition File', 'Model Rendition File'), ('Presentation', 'Presentation'), ('Programme', 'Programme'), ('Register', 'Register'), ('Report', 'Report'), ('Room Data Sheet', 'Room Data Sheet'), ('Schedule', 'Schedule'), ('Specification', 'Specification'), ('Survey', 'Survey'), ('Visualisation', 'Visualisation')], default='2D Drawing', max_length=200),
        ),
        migrations.AddField(
            model_name='drawings',
            name='model_location',
            field=models.CharField(default='Null', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drawings',
            name='paper',
            field=models.CharField(choices=[('A0', 'A0'), ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4')], default='A0', max_length=200),
        ),
        migrations.AddField(
            model_name='drawings',
            name='phase',
            field=models.CharField(default='Design Development', max_length=200),
        ),
        migrations.AddField(
            model_name='drawings',
            name='revision_offset',
            field=models.CharField(default='Null', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drawings',
            name='scale',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('5', '5'), ('10', '10'), ('20', '20'), ('50', '50'), ('100', '100'), ('200', '200'), ('500', '500'), ('1000', '1000'), ('2000', '2000')], default='100', max_length=200),
        ),
        migrations.AddField(
            model_name='drawings',
            name='studio',
            field=models.CharField(choices=[('Sydney', 'Sydney'), ('Melborune', 'Melborune'), ('Perth', 'Perth'), ('Brisbane', 'Brisbane'), ('Canberra', 'Canberra'), ('Adelaide', 'Adelaide'), ('International', 'International')], default='Sydney', max_length=200),
        ),
    ]
