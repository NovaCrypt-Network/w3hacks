# Generated by Django 3.0.7 on 2020-06-07 23:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20200424_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='achievements',
        ),
        migrations.AlterField(
            model_name='profile',
            name='joined_date',
            field=models.DateField(default=datetime.date(2020, 6, 7)),
        ),
        migrations.DeleteModel(
            name='Achievement',
        ),
    ]
