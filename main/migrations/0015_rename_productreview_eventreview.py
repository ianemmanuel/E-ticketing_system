# Generated by Django 3.2.6 on 2021-08-29 16:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_auto_20210829_1942'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductReview',
            new_name='EventReview',
        ),
    ]
