import random

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

    # Show top 5 games on home page
    five_games = []
    if len(games) > 0:
        for i in range(5):
            five_games.append(games[i])
        dict['five_games'] = five_games

    # Show 16 games and news on home page
    games_news = []
    if len(games) > 0:
        gamesId = random.sample(range(0, len(games)), 50)
        count = 0
        for j in gamesId:
            if count == 16:
                break
            else:
                url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + str(
                    games[j].appid) + '&count=1&maxlength=100&format=json'
                api_news = requests.get(url).json()
                if api_news['appnews']['count'] > 0:
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
    # Get id from url
    id = id.replace('/', '')
    game = Game.objects.filter(appid=id)[0]

    # url = 'https://steamspy.com/api.php?request=appdetails&appid=' + id
    # languages = requests.get(url).json()['languages']
    # developer = requests.get(url).json()['developer']

    # These part are used when develop in China
    url = 'https://store.steampowered.com/api/appdetails/?appids=' + id
    languages = requests.get(url).json()[id]['data']['supported_languages'].replace('<strong>*</strong>', '')
    developer = requests.get(url).json()[id]['data']['developers'][0]

    # Get game news from api
    url_news = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=' + id + '&count=10&maxlength=100&format=json'
    news = requests.get(url_news).json()['appnews']['newsitems']

    # Get game screenshots (image link) from api
    url_img = 'https://api.rawg.io/api/games/' + str(game.rawgid) + '/screenshots'
    img = requests.get(url_img).json()['results']

    # Get game details from api
    url_game = 'https://api.rawg.io/api/games/' + str(game.rawgid)
    description = requests.get(url_game).json()['description']
    released = requests.get(url_game).json()['released']
    platforms = requests.get(url_game).json()['platforms']
    genres = requests.get(url_game).json()['genres']

    # Get current login user
    user = request.user
    # Check if current user like this game, and show on web page
    isLike = None
    if user.is_authenticated:
        if Like.objects.filter(user=user, game=game).count() > 0:
            isLike = True
        else:
            isLike = False

    # Check if user already comment twice
    isComment = None
    if user.is_authenticated:
        if Comment.objects.filter(user=user, game=game).count() > 1:
            isComment = True
        else:
            isComment = False

    # Get all comments of the game from database
    if len(Comment.objects.filter(game=game)) > 0:
        comments = Comment.objects.filter(game=game).order_by('-comment_time')
    else:
        comments = None

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
    # /game did not show anything and return to index page
    return render(request, 'web/index.html')


def result(request, search):
    # Get details from url and check
    # if url return anything than search database
    if len(search) > 0:
        search = search.replace('%20', '')
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
    # Ajax for search part
    search = request.POST.get('search')
    if search is not None:
        return HttpResponse(search)
    else:
        return render(request, 'web/search.html')


def searchappid(request):
    # Ajax for search appid part
    try:
        appid = int(request.POST.get('appid'))
        if Game.objects.filter(appid=appid).count() > 0:
            return HttpResponse('OK')
        else:
            return HttpResponse('Game Not Found')
    except ValueError as ve:
        return HttpResponse('Enter Wrong')


def category(request, cat):
    # Show all games in category
    cat = cat.replace('_', ' ')
    game_name = Tag.objects.filter(category__name=cat).values('game__name')
    game_appid = Tag.objects.filter(category__name=cat).values('game__appid')
    games = []
    for i in range(len(game_appid)):
        games.append((game_appid[i]['game__appid'], game_name[i]['game__name']))

    return render(request, 'web/category.html', {'tag': cat, 'games': games})


def like(request):
    # Ajax part when user press like
    appid = request.POST.get('appid')
    user = request.user
    game = Game.objects.filter(appid=appid)[0]
    if Like.objects.filter(user=user, game=game).count() > 0:
        Like.objects.filter(user=user, game=game).delete()
        return HttpResponse('Dislike')
    else:
        # Different from comment, only one like per user
        Like.objects.get_or_create(user=user, game=game)[0].save()
        return HttpResponse('Like')


def comment(request):
    # Ajax part when user comment
    appid = request.POST.get('appid')
    comment = request.POST.get('comment')
    user = request.user
    game = Game.objects.filter(appid=appid)[0]
    # If user already comment once, then the second one will be save and return a message
    # Then the web page will close the comment
    if Comment.objects.filter(user=user, game=game).count() == 1:
        Comment.objects.create(user=user, game=game, comment=comment)
        return HttpResponse('ALREADY COMMENT TWICE')
    # User can't comment if they already done twice
    elif Comment.objects.filter(user=user, game=game).count() > 1:
        return HttpResponse('NO')
    else:
        Comment.objects.create(user=user, game=game, comment=comment)
        return HttpResponse('OK')
