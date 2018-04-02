# Generated by Django 2.0.3 on 2018-03-28 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_experiencecount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mobs', to='api.Location')),
            ],
        ),
        migrations.CreateModel(
            name='MobArsenal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dressed', models.BooleanField(default=False)),
                ('arsenal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mobs', to='api.Arsenal')),
                ('mob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arsenals', to='api.Mob')),
            ],
        ),
    ]