from django.test import TestCase, Client
from guessing_game.models import Room, Player_Guess, Room_Score
from django.urls import reverse
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

# Create your tests here.
class RoomCreationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('home')
        cls.user = USER_MODEL.objects.create_user(
            username='test_user',
            password='!@#qweasd'
        )

    def test_get_home(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_user_must_be_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_single_player_room(self):
        self.client.force_login(self.user)

        room_data = {'room_name':'test_room', 'difficulty': 6, 'player_count': 1}
        response = self.client.post(self.url, data=room_data)
        room_object = Room.objects.get(id=1)
        room_name = room_object.room_name
        master_code_length = len(room_object.master_code)

        self.assertEqual(room_name, 'test_room')
        self.assertEqual(master_code_length, 6)        
        self.assertRedirects(response, '/single-player-room/1/')

    def test_create_multiplayer_room(self):
        self.client.force_login(self.user)

        room_data = {'room_name':'test_room2', 'difficulty': 4, 'player_count': 2}
        response = self.client.post(self.url, data=room_data)
        room_object = Room.objects.get(id=1)
        room_name = room_object.room_name
        master_code_length = len(room_object.master_code)

        self.assertEqual(room_name, 'test_room2')
        self.assertEqual(master_code_length, 4)        
        self.assertRedirects(response, '/multiplayer-room/1/')
    

class GuessValidityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('submit-guess', args=[1])
        cls.user = USER_MODEL.objects.create_user(
            username='test_user',
            password='!@#qweasd'
        )

        Room.objects.create(
            room_name = 'test_room',
            difficulty = 4,
            master_code = '0123',
            player_count = 1,
            completed = False,
        )

    def test_create_valid_guess_correct(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess':'0123'}
        response = self.client.post(self.url, data=guess_data)
        player_guess = Player_Guess.objects.get(id=1)

        self.assertEqual(player_guess.exact_matches, 4)
        self.assertEqual(player_guess.matching_numbers, 4)
        self.assertRedirects(response, '/single-player-room/1/')

    def test_create_valid_guess_incorrect(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': '1234'}
        response = self.client.post(self.url, data=guess_data)
        player_guess = Player_Guess.objects.get(id=1)

        self.assertEqual(player_guess.exact_matches, 0)
        self.assertEqual(player_guess.matching_numbers, 3)
        self.assertRedirects(response, '/single-player-room/1/')

    def test_create_invalid_guess_letters(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': 'asdf'}
        response = self.client.post(self.url, data=guess_data)
        guess_count = Player_Guess.objects.all().count()

        self.assertEqual(guess_count, 0)
        self.assertTemplateUsed(response, 'error_page.html')

    def test_create_invalid_guess_length(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': '123'}
        response = self.client.post(self.url, data=guess_data)
        guess_count = Player_Guess.objects.all().count()

        self.assertEqual(guess_count, 0)
        self.assertTemplateUsed(response, 'error_page.html')

class SinglePlayerGameStateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('single-player-room', args=[1])
        cls.user = USER_MODEL.objects.create_user(
            username='test_user',
            password='!@#qweasd'
        )

        Room.objects.create(
            room_name = 'test_room',
            difficulty = 4,
            master_code = '0123',
            player_count = 1,
        )

        Room.objects.create(
            room_name = 'test_room2',
            difficulty = 4,
            master_code = '0123',
            player_count = 1,
        )

    def setUp(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': '0123'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        guess_data = {'player_guess': '1234'}
        self.client.post(reverse('submit-guess', args=[2]), data=guess_data)
        self.client.get(self.url)

    def test_correct_guess_ending(self):
        room = Room.objects.get(id=1)
        self.assertTrue(room.completed)

    def test_no_remaining_guesses_ending(self):
        for i in range(8):
            guess_data = {'player_guess': '1234'}
            self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
            self.client.get(self.url)
        room = Room.objects.get(id=1)
        self.assertTrue(room.completed)

    def test_game_restart(self):
        self.client.post(reverse('restart-game', args=[1]))
        player_guesses = Player_Guess.objects.filter(user = self.user).count()
        player_score = Room_Score.objects.filter(user = self.user).count()
        self.client.get(self.url)
        room = Room.objects.get(id=1)

        self.assertEqual(player_score, 2)
        self.assertEqual(player_guesses, 1)
        self.assertFalse(room.completed)

    def test_game_delete(self):
        self.client.post(reverse('delete-room', args=[1]))
        player_guesses = Player_Guess.objects.filter(user = self.user).count()
        player_score = Room_Score.objects.filter(user = self.user).count()
        room_count = Room.objects.all().count()

        self.assertEqual(player_score, 1)
        self.assertEqual(player_guesses, 1)
        self.assertEqual(room_count, 1)


class MultiplayerGameStateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('multiplayer-room', args=[1])
        cls.user = USER_MODEL.objects.create_user(
            username='test_user',
            password='!@#qweasd'
        )

        USER_MODEL.objects.create_user(
            username='test_user2',
            password='!@#qweasd'
        )

        room = Room.objects.create(
            room_name = 'test_room',
            difficulty = 4,
            master_code = '0123',
            player_count = 2,
        )

        user2 = USER_MODEL.objects.get(id=2)

        Player_Guess.objects.create(
            user = user2,
            room_id = room,
            player_guess = '1234',
            matching_numbers = 3,
            exact_matches = 0
        )

        Room_Score.objects.create(
            user = user2,
            room_id = room,
            score = 0,
        )

    def test_one_winner_ending(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': '0123'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        self.client.get(self.url)
        room = Room.objects.get(id=1)
        player_score = Room_Score.objects.get(user=self.user).score

        self.assertEqual(player_score, 2)
        self.assertTrue(room.completed)

    def test_tie_ending(self):
        room = Room.objects.get(id=1)
        user2 = USER_MODEL.objects.get(id=2)
        Player_Guess.objects.create(
            user = user2,
            room_id = room,
            player_guess = '0123',
            matching_numbers = 4,
            exact_matches = 4
        )
        self.client.force_login(self.user)
        guess_data = {'player_guess': '1234'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        self.client.get(self.url)
        guess_data = {'player_guess': '0123'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        self.client.get(self.url)
        room = Room.objects.get(id=1)
        player_score = Room_Score.objects.get(user=self.user).score

        self.assertEqual(player_score, 1)
        self.assertTrue(room.completed)


    def test_no_remaining_guesses_ending(self):
        room = Room.objects.get(id=1)
        user2 = USER_MODEL.objects.get(id=2)
        for i in range(9):
            Player_Guess.objects.create(
                user = user2,
                room_id = room,
                player_guess = '1234',
                matching_numbers = 3,
                exact_matches = 0
            )

        self.client.force_login(self.user)
        for i in range(10):
            guess_data = {'player_guess': '1234'}
            self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
            self.client.get(self.url)
        room = Room.objects.get(id=1)
        player_score = Room_Score.objects.get(user=self.user).score

        self.assertEqual(player_score, 0)
        self.assertTrue(room.completed)

    def test_game_delete(self):
        self.client.force_login(self.user)
        self.client.post(reverse('delete-room', args=[1]))
        room_count = Room.objects.all().count()

        self.assertEqual(room_count, 1)

        guess_data = {'player_guess': '0123'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        self.client.get(self.url)

        self.client.post(reverse('delete-room', args=[1]))
        player_score = Room_Score.objects.filter(user = self.user).count()
        player_guesses = Player_Guess.objects.filter(user = self.user).count()
        room_count = Room.objects.all().count()

        self.assertEqual(player_score, 0)
        self.assertEqual(player_guesses, 0)
        self.assertEqual(room_count, 0)

    def test_winner_score_board(self):
        self.client.force_login(self.user)
        guess_data = {'player_guess': '0123'}
        self.client.post(reverse('submit-guess', args=[1]), data=guess_data)
        self.client.get(self.url)