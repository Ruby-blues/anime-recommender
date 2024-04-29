from django.test import TestCase
import requests

# Create your tests here.

# r = requests.get('https://api.jikan.moe/v4/schedules?filter=other')
# r = requests.get('https://api.jikan.moe/v4/schedules?page=4')
# r = requests.get('https://api.jikan.moe/v4/anime?q=Naruto&limit=5')
# for data in r.json()['data']:
#     print(data)
# r = requests.get('https://api.jikan.moe/v4/recommendations/anime?page=1').json()
# print(r)

# r = requests.get('https://api.jikan.moe/v4/top/manga?page=2').json()
# print(r)

# r = requests.get('https://api.jikan.moe/v4/recommendations/manga').json()
# print(r)

# r = requests.get(f'https://api.jikan.moe/v4/manga?type=manhwa')
# print(r.elapsed)

# r = requests.get('https://api.jikan.moe/v4/top/anime').json()

# r = requests.get(f'https://api.jikan.moe/v4/people?q=Mirua, Kentarou').json()['data']
# make a way to redirect when someone clicks a link with a persons name or a studios name
r = requests.get('https://api.jikan.moe/v4/people/16473/full').json()
print(r['data'])

