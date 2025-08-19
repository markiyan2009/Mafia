from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('create/game/', CreateGameView.as_view(), name='add-gammers'),
    path('', ListGamersView.as_view(), name='home'),
    path('set/role/<int:pk>/', SetRoleView.as_view(), name='set-role'),
    path('game/<int:pk>/', GameView.as_view(), name='game'),
    path("check-mafia/", check_mafia_result, name="check_mafia")
]
