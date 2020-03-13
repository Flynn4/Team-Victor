from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
    path('search/', views.search, name='search'),
    re_path(r'game/(\d+)', views.game_info, name='game_info'),
    re_path(r'category/(\S+)', views.category, name='category')
]