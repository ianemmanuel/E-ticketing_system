# Generated by Django 3.2.6 on 2021-09-14 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210908_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
