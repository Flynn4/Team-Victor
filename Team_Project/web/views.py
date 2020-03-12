import random
import urllib

from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import *
import requests
import json
import re


# Create your views here.
def index(request):
    # Add all details into dict
    dict = {}
    games = Game.objects.all()
    dict['games'] = Game.objects.all()
    # dict['categories'] = Category.objects.filter(tag__game_id__lt=2)

    # Show 5 games on home page
    five_games = []
    if len(games) > 0:
        gamesId = random.sample(range(0, len(games)), 5)
        for i in gamesId:
            five_games.append(games[i])
        dict['five_games'] = five_games

    # Show 16 games and news on home page
    games_news = []
    if len(games) > 0:
        gamesId1 = random.sample(range(0, len(games)), 16)
        for j in gamesId1:
            url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(
                games[j].sku) + '&count=3&maxlength=300&format=json'
            api_news_request = requests.get(url)
            api_news = json.loads(api_news_request.content)

            if len(api_news['appnews']['newsitems']) > 0:
                games_news.append((games[j], api_news['appnews']['newsitems'][0]))
            else:
                games_news.append((games[j], None))

        dict['games_news'] = games_news

    # Random show video from database
    videos = Video.objects.all()
    if len(videos) > 0:
        i = random.randint(0, len(videos) - 1)
        dict['video'] = videos[i]

    return render(request, 'web/index.html', dict)


def game_info(request, id):
    url = 'https://steamspy.com/api.php?request=appdetails&appid=' + id
    api_game_request = requests.get(url)
    game = json.loads(api_game_request.content)

    url1 = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + id + '&count=3&maxlength=300&format=json'
    api_news_request = requests.get(url1)
    news = json.loads(api_news_request.content)

    html = urllib.request.urlopen('https://store.steampowered.com/app/' + id).read()
    reg = r'https://steamcdn-a.akamaihd.net/steam/apps/' + id + '/ss_.+?.1920x1080.jpg'
    imglist = re.findall(reg, html.decode('utf-8'))

    return render(request, 'web/game_info.html', {'game': game, 'news': news, 'img': imglist})


def game(request):
    return render(request, 'web/game.html')
