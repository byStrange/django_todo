# Generated by Django 4.0.3 on 2022-06-23 14:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_alter_todo_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2022, 6, 23, 14, 14, 12, 283127, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
    ]
