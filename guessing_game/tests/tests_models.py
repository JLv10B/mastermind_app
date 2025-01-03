from django.test import TestCase
from guessing_game.models import Room, Player_Guess

# Create your tests here.
class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass