# Generated by Django 3.1.7 on 2021-04-24 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0007_auto_20210329_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='leaderboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='leaderboard.leaderboard'),
        ),
    ]
