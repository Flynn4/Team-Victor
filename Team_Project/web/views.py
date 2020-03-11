import random
from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import *
import requests
import json


# Create your views here.
def index(request):

    # Add all details into dict
    dict = {}
    games = Game.objects.all()
    dict['games'] = Game.objects.all()
    dict['categories'] = Category.objects.all()

    # Show 5 games on home page
    five_games = []
    if len(games) > 0:
        gamesId = random.sample(range(0, len(games)), 5)
        for i in gamesId:
            five_games.append(games[i])
        dict['five_games'] = five_games

    # Show 12 games on home page
    games_news = []
    if len(games) > 0:
        gamesId1 = random.sample(range(0, len(games)), 16)
        for j in gamesId1:
            url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(
                games[j].sku) + '&count=3&maxlength=300&format=json'
            api_news_request = requests.get(url)
            api_news = json.loads(api_news_request.content)

            games_news.append((games[j], api_news['appnews']['newsitems'][0]))

        dict['games_news'] = games_news
    print(games_news)

    # Random show video from database
    videos = Video.objects.all()
    if len(videos) > 0:
        i = random.randint(0, len(videos) - 1)
        dict['video'] = videos[i]

    print(dict)
    return render(request, "web/index.html", dict)
