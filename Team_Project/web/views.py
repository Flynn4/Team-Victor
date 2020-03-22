import datetime
import random
import urllib.request

from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
}


# Create your views here.
def index(request):
    # Add all details into dict
    dict = {}
    games = Game.objects.all()
    dict['games'] = Game.objects.all()
    # Already used in template tags
    # dict['categories'] = Category.objects.filter(tag__game_id__lt=2)

    # Show 5 games on home page
    five_games = []
    if len(games) > 0:
        for i in range(5):
            five_games.append(games[i])
        dict['five_games'] = five_games

    # Show 16 games and news on home page
    games_news = []
    gamesId = random.sample(range(0, len(games)), 50)
    if len(games) > 0:
        count = 0
        for j in gamesId:
            if count == 16:
                break
            else:
                url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(
                    games[j].appid) + '&count=3&maxlength=300&format=json'
                api_news = requests.get(url).json()
                if len(api_news['appnews']['newsitems']) > 0:
                    timeStamp = api_news['appnews']['newsitems'][0]['date']
                    dateArray = datetime.datetime.fromtimestamp(timeStamp)
                    otherStyleTime = dateArray.strftime("%d %b %Y")
                    api_news['appnews']['newsitems'][0]['date'] = otherStyleTime
                    games_news.append(api_news['appnews']['newsitems'][0])
                    count += 1
                else:
                    continue

        dict['games_news'] = games_news

    # Random show video from database
    videos = Video.objects.all()
    if len(videos) > 0:
        i = random.randint(0, len(videos) - 1)
        dict['video'] = videos[i]

    return render(request, 'web/index.html', dict)


def game_info(request, id):
    id = id.replace('/', '')
    game = Game.objects.filter(appid=id)[0]

    url = 'https://steamspy.com/api.php?request=appdetails&appid=' + id
    languages = requests.get(url).json()['languages']
    developer = requests.get(url).json()['developer']

    url_news = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + id + '&count=3&maxlength=300&format=json'
    news = requests.get(url_news).json()


    url_img = 'https://api.rawg.io/api/games/' + str(game.rawgid) + '/screenshots'
    img = requests.get(url_img).json()['results']

    url_game = 'https://api.rawg.io/api/games/' + str(game.rawgid)
    description = requests.get(url_game).json()['description']
    released = requests.get(url_game).json()['released']
    platforms = requests.get(url_game).json()['platforms']
    genres = requests.get(url_game).json()['genres']


    return render(request, 'web/game_info.html',
                  {'game': game,
                   'languages': languages,
                   'developer': developer,
                   'news': news,
                   'img': img,
                   'description': description,
                   'released': released,
                   'platforms': platforms,
                   'genres': genres,})


def game(request):
    return render(request, 'web/game.html')


def result(request, search):
    if len(search) > 0:
        games = Game.objects.filter(name__contains=search)
        search_result = []
        for game in games:
            url_game = 'https://api.rawg.io/api/games/' + str(game.rawgid)
            description = requests.get(url_game).json()['description_raw']
            search_result.append((game, description))

        return render(request, 'web/search.html', {'search_result': search_result})
    else:
        return HttpResponse('Enter Wrong!')


def search(request):
    search = request.POST['search']
    if len(search) > 0:
        return HttpResponse(search)
    else:
        return HttpResponse('Wrong')


def searchappid(request):
    appid = request.POST['appid']
    if len(appid) > 0:
        return HttpResponse(appid)
        # return redirect('/game/' + search)
    else:
        return HttpResponse('Enter Wrong!')


def category(request, cat):
    cat = cat.replace('_', ' ')
    game_name = Tag.objects.filter(category__name=cat).values('game__name')
    game_appid = Tag.objects.filter(category__name=cat).values('game__appid')
    games = []
    for i in range(len(game_appid)):
        games.append((game_appid[i]['game__appid'], game_name[i]['game__name']))

    return render(request, 'web/category.html', {'tag': cat, 'games': games})
