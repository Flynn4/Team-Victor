import random
from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):

    # Add all details into dict
    dict = {}
    games = Game.objects.all()
    dict['games'] = Game.objects.all()
    dict['categories'] = Category.objects.all()

    # Show 5 games on home page
    five_games = []
    gamesId = random.sample(range(0, len(games)), 5)
    for i in gamesId:
        five_games.append(games[i])
    dict['five_games'] = five_games

    # Random show video from database
    videos = Video.objects.all()
    i = random.randint(0, len(videos) - 1)
    dict['video'] = videos[i]

    return render(request, "web/index.html", dict)
