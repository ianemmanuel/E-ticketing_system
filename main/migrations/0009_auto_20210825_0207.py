# Generated by Django 3.2.6 on 2021-08-24 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventattribute',
            options={'verbose_name_plural': '6. EventAttributes'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': '7. Profile'},
        ),
    ]