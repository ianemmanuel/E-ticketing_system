# Generated by Django 3.2.6 on 2021-08-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_event_ticket_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='video',
        ),
        migrations.AddField(
            model_name='eventattribute',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos_uploaded'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.CharField(blank=True, default='ticketshop', max_length=400, null=True),
        ),
    ]