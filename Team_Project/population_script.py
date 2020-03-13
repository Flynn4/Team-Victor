import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Team_Project.settings')

import django
import requests
import json

django.setup()
from web.models import *


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    api = requests.get('https://steamspy.com/api.php?request=all').json()
    count = 0
    for i in api:
        if count == 200:
            print(f"\r Adding Games ... Finish!!", end='', flush=True)
            break
        else:
            try:
                api_game = requests.get('https://steamspy.com/api.php?request=appdetails&appid=' + i).json()
                genre = api_game['genre'].split(', ')
                for j in genre:
                    c = add_cat(j)
                    g = add_game(api[i]['name'], api[i]['appid'])
                    add_tag(g, c)
                count += 1
                print(f"\r Adding Games ... [% {count//2}]", end='', flush=True)
            except json.decoder.JSONDecodeError:
                continue

    videos = [
        {'name': 'Half-Life: Alyx Announcement Trailer',
         'videoId': 'O2W0N3uKXmo'},
        {'name': 'Diablo 4 - Official Announcement Cinematic Trailer | Blizzcon 2019',
         'videoId': '0SSYzl9fXOQ'},
        {'name': "Baldur's Gate 3 - Official Opening Cinematic in 4K",
         'videoId': '_hqgv0pU0EM'},
        {'name': 'Cyberpunk 2077 — Official Cinematic Trailer | E3 2019',
         'videoId': 'LembwKDo1Dk'},
        {'name': 'THE LAST OF US 2 Official Trailer (PS4)',
         'videoId': 'qPNiIeKMHyg'}]

    for k in videos:
        add_video(k['name'], k['videoId'])


def add_game(name, appid):
    g = Game.objects.get_or_create(name=name, appid=appid)[0]
    g.save()
    return g


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


def add_tag(game, cat):
    t = Tag.objects.get_or_create(game=game, category=cat)[0]
    t.save()
    return t


def add_video(name, videoId):
    v = Video.objects.get_or_create(name=name, videoId=videoId)[0]
    v.save()
    return v


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
