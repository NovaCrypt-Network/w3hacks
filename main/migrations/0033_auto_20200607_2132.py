# Generated by Django 3.0.7 on 2020-06-08 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20200607_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='max_num_exercises',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='max_num_hackathons',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]