# Generated by Django 3.2.6 on 2021-08-24 18:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210820_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]