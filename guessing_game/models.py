from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    diff_selection = [(4, 'easy'), (5, 'medium'), (6, 'hard')]
    player_count_selection = [(1, 'single player'), (2, 'Multiplayer')]

    room_name = models.CharField(max_length=100, unique=True)
    difficulty = models.IntegerField(choices=diff_selection, default=4)
    player_count = models.IntegerField(choices=player_count_selection, default=1)
    max_number_of_guesses = models.IntegerField(default=10) # don't let this be hard coded in case I want the option to have the player adjust it in the future
    max_score = models.IntegerField(default=10)
    master_code = models.CharField(max_length=8)
    completed = models.BooleanField(default=False)

class Player_Guess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    player_guess = models.CharField(max_length=8)
    matching_numbers = models.IntegerField(default=0)
    exact_matches = models.IntegerField(default=0)


class Room_Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)