# Generated by Django 3.1.7 on 2021-03-28 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0004_auto_20210326_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='status',
        ),
        migrations.AddField(
            model_name='result',
            name='winner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='leaderboard.competitordeck'),
            preserve_default=False,
        ),
    ]
