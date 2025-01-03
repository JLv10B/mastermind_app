from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('register/', views.register_page, name = 'register'),
    path('', views.home_view, name = 'home'),
    path('single-player-room/<str:pk>/', views.single_player_room_view, name = 'single-player-room'),
    path('multiplayer-room/<str:pk>/', views.multiplayer_room_view, name = 'multiplayer-room'),
    path('restart-game/<str:pk>/', views.restart_game, name='restart-game'),
    path('submit-guess/<str:pk>/', views.submit_guess_controller, name='submit-guess'),
    path('error-page/<str:pk>/', views.error_page_view, name='error-page'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    ]