# Generated by Django 3.2.6 on 2024-08-28 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20240828_0048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adddoctor',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='adddoctor',
            name='last_name',
        ),
    ]
