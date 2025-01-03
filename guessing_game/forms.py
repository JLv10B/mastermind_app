from django.forms import ModelForm
from .models import Room, Player_Guess

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'player_count', 'difficulty']

class PlayerGuessForm(ModelForm):
    class Meta:
        model = Player_Guess
        fields = ['player_guess']