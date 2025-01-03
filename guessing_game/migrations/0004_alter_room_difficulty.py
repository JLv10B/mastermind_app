# Generated by Django 4.2.4 on 2024-12-31 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guessing_game', '0003_alter_room_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='difficulty',
            field=models.IntegerField(choices=[(4, 'easy'), (5, 'medium'), (6, 'hard')], default=4, max_length=6),
        ),
    ]
