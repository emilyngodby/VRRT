# Generated by Django 3.1.5 on 2021-01-16 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VRRTController', '0006_auto_20210115_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteid',
            name='SiteTelephone',
            field=models.CharField(default='NOT SET', help_text='Enter the site telephone number', max_length=200),
        ),
    ]
