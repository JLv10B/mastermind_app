from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Player_Guess, Room_Score
from .forms import RoomForm, PlayerGuessForm
import requests
import json
import re

# Create your views here.
def user_login(request):
    """"
    This function allows user to login

    """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def user_logout(request):
    """ 
    This function allows users to log out.
    
    """
    logout(request)
    return redirect('home')


def register_page(request):
    """
    This function allows users to register a profile, then redirects them to the home page after logging in.

    """
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
          user = form.save(commit=False)  
          user.username = user.username.lower()
          user.save()
          login(request, user)
          return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form}
    return render(request, 'login_register.html', context)


def random_pattern_generator(pattern_length):
    """
    This function generates a random pattern using the random number generator API(https://www.random.org/clients/http/api/). The expected response from the API is a JSON object with nested dictionary. If the reponse is successful then we can return the master_code.
    
    example:
    Input: 4
    Output:'1234'
    
    """
    api_key = '6802e62a-b150-4821-ab25-8f0c637480fb'
    url = 'https://api.random.org/json-rpc/4/invoke'
    data = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": pattern_length,
            "min": 0,
            "max": 7,
            "replacement": True
        },
        "id": 1
        }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        pattern = response.json()
        numbers = pattern['result']['random']['data']
        master_code = ''.join(str(x) for x in numbers)
        return master_code
    else:
        return 'Error making master code'

    
def validate_player_input(player_input, pattern_length):
    """
    This function validates player input. Player input should only contain numbers and be the length determined by pattern_length. If the player's input is valid then return True else return False

    Input:
        player_input = '1123'
    Output:
        True

    """
    if not re.search(r'^[0-7]*$', player_input):
        return False, "That's not a valid guess, only numbers 0-7 please!"
    elif len(player_input) != pattern_length:
        return False, f"That's not a valid guess, I need {pattern_length} numbers!"
    else:
        return True, ''
    

def find_matching_and_exact_matches(player_guess, master_code):
    """
    This function takes a player's guess and compares it to the master code. It returns 2 integers, the first representing the number of mastching numbers and the second is the amout of exact matches.
    
    Example:
    Input:
        mastercode = '1234'
        player_guess = '0204'
    Output:
        2,2

    """
    matching_numbers = [x for x in player_guess if x in master_code]
    exact_matches  = 0
    for i in range(len(player_guess)):
        if master_code[i] == player_guess[i]:
            exact_matches += 1
    
    return len(matching_numbers), exact_matches


def player_feedback(user, room_id):
    """
    This function accepts a user object and room_id and returns a list of responses.

    Example:
    Input: <user1_obj>
    Output: ["Guess #1: 1234 || You guessed {x} correct number(s) and have {y} exact matche(s)", ...]

    """
    previous_guesses = user.player_guess_set.filter(room_id = room_id)
    previous_guess_feedback = []
    guess_count = 0
    for guess in previous_guesses:
        if guess.matching_numbers > 1 or guess.matching_numbers == 0:
            number = 'numbers'
        else:
            number = 'number'
        if guess.exact_matches > 1 or guess.exact_matches == 0:
            match = 'matches'
        else:
            match = 'match'
        guess_count += 1
        previous_guess_feedback.append(f'Guess #{guess_count}: {guess.player_guess} || You guessed {guess.matching_numbers} correct {number} and have {guess.exact_matches} exact {match}.')

    return previous_guess_feedback


def create_room_score(request,pk):
    """
    This function accepts a POST request and creates a new room_score object
    
    """
    if request.method == "POST":
        user = request.user
        room = Room.objects.get(id=pk)
        Room_Score.objects.create(
            user = user,
            room_id = room
        )
        return

@login_required(login_url='/login')
def home_view(request):
    """
    This view renders the home page with login/logout functions. The player can create a room with a room name and selected difficulty. After the room is created the player is redirected to the created room page. This view should include a form to create a room, a list of all current rooms, and a welcome message.
    
    """
    form = RoomForm()
    return_message = ["Welcome! Name your room and select your difficulty"]

    if request.method == "POST":
        user_room_name = request.POST.get('room_name')
        selected_difficulty = int(request.POST.get('difficulty'))
        player_count = request.POST.get('player_count')
        generated_pattern = random_pattern_generator(selected_difficulty)
        
        if generated_pattern == 'Error making master code':
            return_message = ["An Error occured during room creation"]
        else:
            room = Room.objects.create(
                room_name = user_room_name,
                player_count = player_count,
                difficulty = selected_difficulty,
                master_code = generated_pattern,
                )
            create_room_score(request, room.id)
            if player_count == '1':
                return redirect('single-player-room', pk=room.id)
            else:
                return redirect('multiplayer-room', pk=room.id)

    user_in_room = Room_Score.objects.filter(user = request.user)
    user_single_rooms = []
    for room in user_in_room:
        if room.room_id.player_count == 1:
            user_single_rooms.append(room.room_id)
    multiplayer_rooms = Room.objects.filter(player_count=2)
    context = {'form':form, 'user_single_rooms':user_single_rooms, 'return_messages':return_message, 'multiplayer_rooms': multiplayer_rooms}
    return render(request, 'home.html', context)


def generate_guess(request, pk):
    """
    This function accepts a POST request and validates the player's input. If the player's input is not valid then it will return False and an error message. If the input is valid then the function will return True. If the input is valid the function creates a player_guess object and check if the player already has a Room_score object associated with them, if not it will be created.

    Input: HTTPrequest, pk
    Output: True, 'error message'

    """
    error_message = 'No errors here'
    room = Room.objects.get(id = pk)
    difficulty = room.difficulty
    master_code = room.master_code

    if request.method == "POST":
        player_input = request.POST.get('player_guess')
        input_valid, error_message = validate_player_input(player_input, difficulty)

    if input_valid == True:
        matching, exact = find_matching_and_exact_matches(player_input, master_code)
        Player_Guess.objects.create(
            user = request.user,
            room_id = room,
            player_guess = player_input,
            matching_numbers = matching,
            exact_matches = exact
        )

    try:
        Room_Score.objects.filter(user = request.user).get(room_id=room)
    except:
        create_room_score(request, room.id)
    
    return input_valid, error_message


@login_required(login_url='/login')
def single_player_room_view(request, pk):
    """
    This view renders a singleplayer room and manages the room.completed state. If the player has correctly guessed the master code or reached the maxium number of guesses, the room should be marked at completed. This view should render the all the previous guesses along with their appropriate feedback, guess count, form to allow the player to submit a guess, and room name.

    """
    form = PlayerGuessForm()
    room = Room.objects.get(id = pk)
    room_scores = Room_Score.objects.filter(room_id = room)
    score_board = room_scores.order_by('-score')
    previous_guesses = room.player_guess_set.filter(user = request.user)
    guess_count = previous_guesses.count()
    remaining_guesses = room.max_number_of_guesses - guess_count
    previous_guess_feeback = player_feedback(request.user, pk)
    room_feedback =f'Please enter a {room.difficulty} digit number, digits must be 0-7'

    try:
        request.user.player_guess_set.filter(room_id=pk).get(exact_matches = room.difficulty)
        room_feedback =f'Congratulations {request.user}, you win!'
        room.completed = True
        player_score = room_scores.get(user = request.user)
        player_score.score += 1
        room.save()
        player_score.save()        
    except:
        if remaining_guesses <= 0:
            room_feedback = 'You have no more guesses left.\n Would you like to play again?'
            room.completed = True
            room.save()
        
    context = {'room':room, 'form':form, 'score_board':score_board, 'previous_guess_feeback':previous_guess_feeback, 'return_message': room_feedback, 'remaining_guesses': remaining_guesses}
    return render(request, 'room.html', context)


@login_required(login_url='/login')
def multiplayer_room_view(request, pk):
    """
    This view renders a multiplayer room and manages when the game is completed. If the player has correctly guessed the master code or reached the maxium number of guesses, the points should be distributed to the correct players and room should be marked at completed, players will no longer be able to submit guesses. The view should include the all the previous guesses along with their appropriate feedback, guess count, form to allow the player to submit a guess, scoreboard, and room name.

    """
    form = PlayerGuessForm()
    room = Room.objects.get(id = pk)
    room_scores = Room_Score.objects.filter(room_id = room)
    score_board = room_scores.order_by('-score')
    difficulty = room.difficulty
    previous_guesses = room.player_guess_set.filter(user = request.user)
    guess_count = previous_guesses.count()
    remaining_guesses = room.max_number_of_guesses - guess_count
    previous_guess_feeback = player_feedback(request.user, pk)
    room_feedback =f'Please enter a {difficulty} digit number, digits must be 0-7'
    participants_guess_count = room_participants_and_guess_count(pk)

    if len(participants_guess_count) > 1 and min(participants_guess_count.values()) > 0: # If there are >1 participants and each has at least 1 guess, check for a winner
        correct_guesses = room.player_guess_set.filter(exact_matches = room.difficulty)
        correct_players = []
        lowest_guess_count = min(participants_guess_count.values())
        for guesses in correct_guesses:
            if participants_guess_count[guesses.user] <= lowest_guess_count: # If a player enter the room late and the game hasn't ended yet, they get to have the same # of guesses
                correct_players.append(guesses.user)

        GAME_STILL_RUNNING = 0
        WINNER = 1
        TIE = 2
        NO_WINNER = 3
        result = GAME_STILL_RUNNING  

        if len(correct_players) == 1: 
            room_feedback =f'{correct_players[0]} is the winner!'
            result = WINNER
        elif len(correct_players) > 1:
            tied_users = [player.username for player in correct_players]
            room_feedback =f"It's a tie between {', '.join(map(str,tied_users))}!"
            result = TIE
        elif lowest_guess_count == room.max_number_of_guesses:
            room_feedback =f"Everyone is out of guesses, there is no winner."
            result = NO_WINNER
        
        if room.completed == False and result != GAME_STILL_RUNNING:
            if result == WINNER:
                player_score = room_scores.get(user = correct_players[0])
                player_score.score += 2
                player_score.save()
            elif result == TIE:
                for player in correct_players:
                    player_score = room_scores.get(user = player)
                    player_score.score += 1
                    player_score.save()
            room.completed = True
            room.save()

    context = {'room':room, 'form':form, 'score_board':score_board, 'previous_guess_feeback':previous_guess_feeback, 'return_message': room_feedback, 'remaining_guesses': remaining_guesses}
    return render(request, 'room.html', context)


@login_required(login_url='/login')
def submit_guess_controller(request, pk):
    """
    This function controls which logic is applied to guess submission requests. Passes the POST request and pk to single player and multiplayer submit guess functions.
    
    """
    room = Room.objects.get(id=pk)
    if room.player_count == 1:
        return singe_player_submit_guess(request, pk)
    else:
        return multiplayer_submit_guess(request, pk)


def singe_player_submit_guess(request, pk):
    """
    This function dictates the logic for when guesses are allowed to be submitted for single player rooms. Players are not able to submit a guess if the room has been marked completed or if they have no more remaining guesses. 

    """
    room = Room.objects.get(id=pk)
    participants_guess_count = room_participants_and_guess_count(pk)
    if request.user not in participants_guess_count:
        participants_guess_count[request.user] = 0
    remaining_guesses = room.max_number_of_guesses - participants_guess_count[request.user]

    if room.completed == True or remaining_guesses <= 0: 
        return redirect('single-player-room', pk=pk)
    
    is_valid, error_message = generate_guess(request, pk)

    if is_valid == False:
        context = {'error_message':error_message}
        return render(request, 'error_page.html', context)
    return redirect('single-player-room', pk=pk)

    
def multiplayer_submit_guess(request, pk):
    """
    This function dictates the logic for when guesses are allowed to be submitted for multiplayer rooms. Players cannot submit guesses if they have 1 or more guesses than the player with the fewest guesses. Eg. A player should not be able to submit their 7th guess until everyone in the room has submitted their 6th guess. Accepts a POST request and passes it to the submit_guess function.

    """
    room = Room.objects.get(id=pk)
    participants_guess_count = room_participants_and_guess_count(pk)

    if request.user not in participants_guess_count: # The user isn't a participant until they have submitted a guess so we have to add the user manually to the dict
        participants_guess_count[request.user] = 0

    remaining_guesses = room.max_number_of_guesses - participants_guess_count[request.user]

    if room.completed == True or remaining_guesses <= 0 or len(participants_guess_count) <= 1: # Can't submit a guess if only 1 player in a multiplayer room
        return redirect('multiplayer-room', pk=pk)

    lowest_guess_count = min(participants_guess_count.values())

    if participants_guess_count[request.user] <= lowest_guess_count:
        is_valid, error_message = generate_guess(request, pk)
        if is_valid == False:
            context = {'error_message':error_message}
            return render(request, 'error_page.html', context)
        else:
            return redirect('multiplayer-room', pk=pk)
    return redirect('multiplayer-room', pk=pk)
    

def room_participants_and_guess_count(room_id):
    """
    This functions accepts the room id and returns a dictionary of all user object in the room and their guess counts {user:guess_count}.

    Example:
    Input: 1
    Output: {<user1_obj>:3, <user2_obj>:3, <user3_obj>:2}

    """
    room = Room.objects.get(id=room_id)
    scores = Room_Score.objects.filter(room_id = room)
    participant_list = [user.user for user in scores]
    participant_guess_dict = {}
    for player in participant_list:
        guess_count = room.player_guess_set.filter(user=player).count()
        participant_guess_dict[player] = guess_count

    return participant_guess_dict


@login_required(login_url='/login')
def error_page_view(request, pk):
    """
    This view renders an error page along with the appropriate message. Player should be able to return back to the room that they were in when the error occured.

    """
    room = Room.objects.get(id = pk)
    error_message = ''

    context = {'room':room, 'error_message':error_message}
    return render(request, 'error_page.html', context)


@login_required(login_url='/login')
def restart_game(request, pk):
    """
    This function allows the player to restart the game with a new master code. It deletes all guesses linked to the room.

    """
    room = Room.objects.get(id = pk)
    guesses = Player_Guess.objects.filter(room_id = pk)
    if request.method == "POST" and room.completed == True:
        guesses.delete()
    
        generated_pattern = random_pattern_generator(room.difficulty)
        room.master_code = generated_pattern
        room.completed = False
        room.save()

    if room.player_count == 1:
        return redirect('single-player-room', pk=pk)
    else:
        return redirect('multiplayer-room', pk=pk)


@login_required(login_url='/login')
def delete_room(request, pk):
    """
    This function allows users to delete rooms. If it is a single player room then the player can delete it at any time. If it's a multiplayer room then the room can only be deleted if the room status is set to completed.
    
    """
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        if room.player_count == 1:
            room.delete()
            Player_Guess.objects.filter(room_id=room).delete()
            Room_Score.objects.filter(room_id=room).delete()
            return redirect('home')
        else:
            if room.completed == True:
                room.delete()
                Player_Guess.objects.filter(room_id=room).delete()
                Room_Score.objects.filter(room_id=room).delete()
                return redirect('home')
            else:
                return redirect('multiplayer-room', pk=pk)
