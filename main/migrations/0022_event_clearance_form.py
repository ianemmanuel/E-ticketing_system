# Generated by Django 3.2.6 on 2021-10-07 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_eventattribute_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='Clearance_Form',
            field=models.FileField(blank=True, null=True, upload_to='clearance_uploaded/'),
        ),
    ]
