# Generated by Django 4.0.5 on 2022-07-04 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_alter_userlist_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]