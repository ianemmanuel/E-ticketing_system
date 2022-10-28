# Generated by Django 3.2.6 on 2021-09-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes'),
        ),
        migrations.AlterField(
            model_name='eventattribute',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos_uploaded/'),
        ),
    ]
