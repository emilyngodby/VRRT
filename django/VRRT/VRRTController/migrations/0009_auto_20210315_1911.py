# Generated by Django 3.1.7 on 2021-03-15 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VRRTController', '0008_auto_20210315_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyinstance',
            name='ReperationRateEnd',
        ),
        migrations.RemoveField(
            model_name='surveyinstance',
            name='ReperationRateStart',
        ),
    ]
