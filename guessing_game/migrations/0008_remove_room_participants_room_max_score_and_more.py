# Generated by Django 4.2.4 on 2025-01-02 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guessing_game', '0007_alter_player_guess_exact_matches_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='participants',
        ),
        migrations.AddField(
            model_name='room',
            name='max_score',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='room',
            name='player_count',
            field=models.IntegerField(choices=[(1, 'single player'), (2, 'Multiplayer')], default=1),
        ),
        migrations.AlterField(
            model_name='player_guess',
            name='player_guess',
            field=models.CharField(max_length=8),
        ),
        migrations.CreateModel(
            name='Room_Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guessing_game.room')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]