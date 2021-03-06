# Generated by Django 3.0.3 on 2020-02-19 06:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tutorial_title', models.CharField(max_length=200)),
                ('tutorial_content', models.TextField()),
                ('tutorial_published', models.DateTimeField(default=datetime.datetime(2020, 2, 19, 17, 35, 52, 449167), verbose_name='date published')),
                ('slug', models.CharField(default='1', max_length=200)),
            ],
        ),
    ]
