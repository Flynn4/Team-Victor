from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
    re_path(r'^game/(\d+.)$', views.game_info, name='game_info'),
    re_path(r'^category/(\S+.)$', views.category, name='category'),
    path('searchappid/', views.searchappid, name='searchappid'),
    re_path(r'^search/(\S+.)$', views.result, name='result'),
    path('search/', views.search, name='search'),
    path('like/', views.like, name='like'),
    path('comment/', views.comment, name='comment'),
]