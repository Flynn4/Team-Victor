import json
import time

import requests
from slugify import slugify
import re


text = 'Gotham City Impostors: Free To Play'
text = slugify(text)
print(text)

url_game = 'https://api.rawg.io/api/games/batman-aa-goty'
description = requests.get(url_game).json()['description']
released = requests.get(url_game).json()['released']
platforms = requests.get(url_game).json()['platforms']
stores = requests.get(url_game).json()['stores']
url = 'http://store.steampowered.com/app/35140/'
print(stores)
for i in stores:
    if url == i['url']:
        print('yes')
    else:
        print('shit')

appid = re.findall('(\d+)', url)[0]
print(appid)