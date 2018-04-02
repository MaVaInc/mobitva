# Generated by Django 2.0.3 on 2018-03-28 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_mob_mobarsenal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mob',
            name='location',
        ),
        migrations.AddField(
            model_name='mob',
            name='location',
            field=models.ManyToManyField(related_name='mobs', to='api.Location'),
        ),
    ]