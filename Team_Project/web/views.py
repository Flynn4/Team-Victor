import datetime
import random

from django.db.models import F
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
                    games[j].appid) + '&count=1&maxlength=100&format=json'
                api_news = requests.get(url).json()['appnews']['newsitems']
                if len(api_news) > 0:
                    games_news.append(api_news[0])
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

    # Can't use in China
    # url = 'https://steamspy.com/api.php?request=appdetails&appid=' + id
    # languages = requests.get(url).json()['languages']
    # developer = requests.get(url).json()['developer']

    url = 'https://store.steampowered.com/api/appdetails/?appids=' + id
    languages = requests.get(url).json()[id]['data']['supported_languages'].replace('<strong>*</strong>', '')
    developer = requests.get(url).json()[id]['data']['developers'][0]

    url_news = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + id + '&count=10&maxlength=100&format=json'
    news = requests.get(url_news).json()['appnews']['newsitems']

    url_img = 'https://api.rawg.io/api/games/' + str(game.rawgid) + '/screenshots'
    img = requests.get(url_img).json()['results']

    url_game = 'https://api.rawg.io/api/games/' + str(game.rawgid)
    description = requests.get(url_game).json()['description']
    released = requests.get(url_game).json()['released']
    platforms = requests.get(url_game).json()['platforms']
    genres = requests.get(url_game).json()['genres']

    user = request.user
    isLike = None
    if user.is_authenticated:
        if Like.objects.filter(user=user, game=game).count() > 0:
            isLike = True
        else:
            isLike = False

    if len(Comment.objects.filter(game=game)) > 0:
        comments = Comment.objects.filter(game=game).order_by('-comment_time')
    else:
        comments = None

    isComment = None
    if user.is_authenticated:
        if Comment.objects.filter(user=user, game=game).count() > 1:
            isComment = True
        else:
            isComment = False

    return render(request, 'web/game_info.html',
                  {'game': game,
                   'languages': languages,
                   'developer': developer,
                   'news': news,
                   'img': img,
                   'description': description,
                   'released': released,
                   'platforms': platforms,
                   'genres': genres,
                   'isLike': isLike,
                   'isComment': isComment,
                   'comments': comments})


def game(request):
    return render(request, 'web/index.html')


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


def like(request):
    appid = request.POST['appid']
    user = request.user
    game = Game.objects.filter(appid=appid)[0]
    if Like.objects.filter(user=user, game=game).count() > 0:
        Like.objects.filter(user=user, game=game).delete()
        return HttpResponse('Dislike')
    else:
        Like.objects.get_or_create(user=user, game=game)[0].save()
        return HttpResponse('Like')


def comment(request):
    appid = request.POST['appid']
    comment = request.POST['comment']
    user = request.user
    game = Game.objects.filter(appid=appid)[0]
    if Comment.objects.filter(user=user, game=game).count() == 1:
        Comment.objects.create(user=user, game=game, comment=comment)
        return HttpResponse('ALREADY COMMENT TWICE')
    elif Comment.objects.filter(user=user, game=game).count() > 1:
        return HttpResponse('NO')
    else:
        Comment.objects.create(user=user, game=game, comment=comment)
        return HttpResponse('OK')
