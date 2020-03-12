from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
    re_path(r'^game/(\d+)/$', views.game_info, name='game_info'),
]