# Generated by Django 3.0.3 on 2020-04-01 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drawingregister', '0042_projects_namingconv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drawings',
            name='discipline',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_discipline',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_level',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_originator',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_project',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_series',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_type',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_volume_system',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dn_zone_sequence',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='drawing_title1',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='drawing_title2',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='drawing_title3',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='dwg_type',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='model_location',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='originator',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='paper',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='phase',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='revision_offset',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='scale',
        ),
        migrations.RemoveField(
            model_name='drawings',
            name='studio',
        ),
    ]
