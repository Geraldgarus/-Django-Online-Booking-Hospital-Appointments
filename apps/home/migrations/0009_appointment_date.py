# Generated by Django 3.2.6 on 2024-08-27 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20240827_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=datetime.date(2024, 8, 27)),
            preserve_default=False,
        ),
    ]
