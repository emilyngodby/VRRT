# Generated by Django 3.1.3 on 2020-11-30 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VRRTController', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyinstance',
            name='PainScoreEnd',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='surveyinstance',
            name='PainScoreStart',
            field=models.IntegerField(),
        ),
    ]