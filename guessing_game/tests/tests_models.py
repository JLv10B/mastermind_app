from django.test import TestCase
from guessing_game.models import Room, Player_Guess, Room_Score
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

# Create your tests here.
class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room_name = 'test_room'
        cls.difficulty = 4
        cls.player_count = 1

    def test_create_room(self):
        Room.objects.create(
            room_name = self.room_name,
            difficulty = self.difficulty,
            player_count = self.player_count,
        )

        room = Room.objects.get(id=1)
        self.assertEqual(room.room_name, 'test_room')
        self.assertEqual(room.difficulty, 4)
        self.assertEqual(room.player_count, 1)
        self.assertEqual(room.max_number_of_guesses, 10)
        self.assertEqual(room.max_score, 10)
        self.assertFalse(room.completed)

class PlayerGuessModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(
            room_name = 'test_room',
            difficulty = 4,
            player_count = 1,
            master_code = '1234'
        )

        cls.user = USER_MODEL.objects.create(
            username = 'test_user',
            password = '!@#qweasd'
        )

    def test_create_player_guess(self):
        Player_Guess.objects.create(
            user = self.user,
            room_id = self.room,
            player_guess = '1234',
            matching_numbers = 4,
            exact_matches = 4,
        )

        guess = Player_Guess.objects.get(id=1)
        self.assertEqual(guess.user, self.user)
        self.assertEqual(guess.room_id, self.room)
        self.assertEqual(guess.player_guess, '1234')
        self.assertEqual(guess.matching_numbers, 4)
        self.assertEqual(guess.exact_matches, 4)

class RoomScoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room = Room.objects.create(
            room_name = 'test_room',
            difficulty = 4,
            player_count = 1,
            master_code = '1234'
        )

        cls.user = USER_MODEL.objects.create(
            username = 'test_user',
            password = '!@#qweasd'
        )

    def test_create_room_score(self):
        Room_Score.objects.create(
            user = self.user,
            room_id = self.room,
            score = 10,
        )

        room_score = Room_Score.objects.get(id=1)
        self.assertEqual(room_score.user, self.user)
        self.assertEqual(room_score.room_id, self.room)
        self.assertEqual(room_score.score, 10)
        
    
        