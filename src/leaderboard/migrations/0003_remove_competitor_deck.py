# Generated by Django 3.1.7 on 2021-03-25 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0002_auto_20210322_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitor',
            name='deck',
        ),
    ]
