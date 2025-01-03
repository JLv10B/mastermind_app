<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />

<h3 align="center">Mastermind app</h3>

  <p align="center">
    A web based mastermind game for you and your friends! 
    <br />
    <a href="https://github.com/JLv10B/mastermind_app"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The mastermind app is a web based mastermind game, which can be played against the computer. This is a game where a you try to guess a randomly generated number combination aka. master code. At the end of each attempt to guess the master code, the computer will provide feedback on how many numbers you have guessed correctly, as well as how many exact matches. You must guess the right number combination within 10 attempts to win the game. The app supports both single player play against the computer with varying difficulty. The app also supports multiplayer play where players compete to guess the master code before their competitors, again with varying levels of difficulty. The mastermind app is built on the django web framework using python for the backend and HTML for the front end.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Django
* Python 3.11.3

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
### Prerequisites


* Django
* Djangorestframework
* requests
  ```sh
  pip install django
  pip install djangorestframework
  pip install requests
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/JLv10B/mastermind_app.git
   ```
2. Install NPM packages
  ```sh
  pip install django
  pip install djangorestframework
  pip install requests
  ```
3. Make migrations
  ```sh
  python manage.py makemigrations
  ```
4. Migrate
  ```sh
  python manage.py migrate
  ```
5. Runserver
  ```sh
  python manage.py runserver
  ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Creating a room
* First register an account
* Once registered and logged in you can create a new room by entering a name for the room, selecting if it's going to be a single player or multiplayer room, and choosing the difficulty

Single player
* Submit any 4-6 digit number (depending on the difficulty), digits must be 0-7
* Once your guess has been submitted your guess and feedback will populate onto the screen
* The game is completed once you have guessed the master code or you have run out of guesses
* Once the game is completed you can restart the game with a new master code
* You can delete the room at any point and return to the home page

Multiplayer
* Similar to single player gameplay but you cannot submit any guesses until there is another player in the room
* The player that did not create the room must guess first to eliminate any unfair advantage
* Each player must wait until each guessing round completes before entering their next guess
* Players will not be able to get further ahead by guessing faster
* Rounds can end with a winner, tie, or no winners
* The player who guesses the master code in the fewest guesses is the winner and scores 2 points
* If multiple players guess the master code in the same number of guesses then those players are tied and each player scores 1 point
* If no player guesses the master code within 10 guesses, the round ends and no one gets any points
* Rounds can be reset after they are completed, scores carry over to each round but not between rooms
* Rooms can be deleted after any round is completed


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Allow more configuration for multiplayer rooms
- [ ] Allow for different types of multiplayer modes
- [ ] Timed rounds
- [ ] Player power features that affect other players

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

James Liaw- jamesliaw10@gmail.com

Project Link: [https://github.com/JLv10B/mastermind_app](https://github.com/JLv10B/mastermind_app)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


