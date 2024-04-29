import requests
from animelist.models import MangaWatchLater, AnimeWatchLater, Liked, MangaGenres, AnimeGenres
from datetime import date


def anime_list(anime='', page=1, types='', status='', genres='', min_score='', max_score='', rating='', user=None):
    animes = []
    page_data = []
    seen_ids = set()
    if anime:
        r = requests.get(f'https://api.jikan.moe/v4/anime?q={anime}')
    else:
        r = requests.get(f'https://api.jikan.moe/v4/anime?q='
                         f'{anime}&page={page}&type={types}&status={status}&genres={genres}&min_score={min_score}'
                         f'&max_score={max_score}&rating={rating}&order_by=popularity&sort=asc')
    for anime_data in r.json()['data']:
        mal_id = anime_data['mal_id']
        if mal_id not in seen_ids:
            animes.append({
                'status': r.status_code,
                'exceptions': r,
                'type': 'anime',
                'like': False,
                'later': False,
                'mal_id': anime_data['mal_id'],
                'img': anime_data['images']['webp']['large_image_url'],
                'default_title': anime_data['title'],
                'english_title': anime_data['title_english'],
                'episode': anime_data['episodes'],
                'ongoing': anime_data['airing'],
                'score': anime_data['score'],
            })
            seen_ids.add(mal_id)
    page_data.append({'last_page': r.json()['pagination']['last_visible_page'],
                      'next_page': r.json()['pagination']['has_next_page']})
    compare_many(AnimeWatchLater.objects, animes, 'later', user)
    compare_many(Liked.objects, animes, 'like', user)
    return animes, page_data


def top_anime(page=1, types='', filters='', rating='', user=None):
    animes = []
    page_data = []

    r = requests.get(f'https://api.jikan.moe/v4/top/anime?page={page}&type={types}&filter={filters}&rating={rating}')
    for anime_lst in r.json()['data']:
        # if anime_lst['title'] or anime_lst['default_title']  do something about long anime names and make the
        # custom list page for each anime and fix the search bar
        animes.append({
            'status': r.status_code,
            'exceptions': r,
            'type': 'anime',
            'like': False,
            'later': False,
            'mal_id': anime_lst['mal_id'],
            'img': anime_lst['images']['webp']['large_image_url'],
            'default_title': anime_lst['title'],
            'english_title': anime_lst['title_english'],
            'episode': anime_lst['episodes'],
            'ongoing': anime_lst['airing'],
            'score': anime_lst['score'],
        })
    page_data.append({'last_page': r.json()['pagination']['last_visible_page'],
                      'next_page': r.json()['pagination']['has_next_page']})
    compare_many(AnimeWatchLater.objects, animes, 'later', user)
    compare_many(Liked.objects, animes, 'like', user)
    return animes, page_data


def anime_random(user):
    animes = []
    request = requests.get('https://api.jikan.moe/v4/random/anime')
    anime_data = request.json()['data']
    if request.status_code == 200:
        animes.append({
            'status': request.status_code,
            'exceptions': request,
            'mal_id': anime_data['mal_id'],
            'url': anime_data['url'],
            'type': 'anime',
            'like': False,
            'later': False,
            'source': anime_data['source'],
            'img': anime_data['images']['webp']['large_image_url'],
            'trailer': anime_data['trailer']['url'],
            'thumbnail': anime_data['trailer']['images']['small_image_url'],
            'default_title': anime_data['title'],
            'english_title': anime_data['title_english'],
            'japanese_title': anime_data['title_japanese'],
            'episode': anime_data['episodes'],
            'ongoing': anime_data['airing'],
            'airing': anime_data['status'],
            'aired_from': anime_data['aired']['from'],
            'aired_to': anime_data['aired']['to'],
            'duration': anime_data['duration'],
            'rated': anime_data['rating'],
            'score': anime_data['score'],
            'scored_by': anime_data['scored_by'],
            'rank': anime_data['rank'],
            'popularity': anime_data['popularity'],
            'favorites': anime_data['favorites'],
            'titles': [(name['type'], name['title']) for name in anime_data['titles']],
            'producers': [(pro['name'], pro['url']) for pro in anime_data['producers']],
            'licensors': [(lic['name'], lic['url']) for lic in anime_data['licensors']],
            'studios': [(stu['name'], stu['url']) for stu in anime_data['studios']],
            'genres': [(genre['name'], genre['url']) for genre in anime_data['genres']],
            'demographics': [(demo['name'], demo['url']) for demo in anime_data['demographics']],
            'synopsis': anime_data['synopsis'],
        })
        animes[0]['later'] = compare(AnimeWatchLater.objects, animes[0]['mal_id'], 'later', user=user)
        animes[0]['like'] = compare(Liked.objects, f'{animes[0]["mal_id"]}{animes[0]["type"]}', 'like', user=user)
        return animes
    elif request.status_code in [404, 400, 500, 429, 405]:
        return animes.append({'status': request.json()['status'], 'message': request.json()['message']})


def get_anime(mal_id, user):
    animes = []
    request = requests.get(f'https://api.jikan.moe/v4/anime/{mal_id}/full')
    anime_data = request.json()['data']
    animes.append({
        'status': request.status_code,
        'exceptions': request,
        'mal_id': anime_data['mal_id'],
        'url': anime_data['url'],
        'type': 'anime',
        'media_type': anime_data['type'],
        'like': False,
        'later': False,
        'source': anime_data['source'],
        'img': anime_data['images']['webp']['large_image_url'],
        'trailer': anime_data['trailer']['url'],
        'thumbnail': anime_data['trailer']['images']['small_image_url'],
        'default_title': anime_data['title'],
        'english_title': anime_data['title_english'],
        'japanese_title': anime_data['title_japanese'],
        'episode': anime_data['episodes'],
        'ongoing': anime_data['airing'],
        'airing': anime_data['status'],
        'aired_from': anime_data['aired']['from'],
        'aired_to': anime_data['aired']['to'],
        'duration': anime_data['duration'],
        'rated': anime_data['rating'],
        'score': anime_data['score'],
        'scored_by': anime_data['scored_by'],
        'rank': anime_data['rank'],
        'popularity': anime_data['popularity'],
        'favorites': anime_data['favorites'],
        'titles': [(name['type'], name['title']) for name in anime_data['titles']],
        'producers': [(pro['name'], pro['url']) for pro in anime_data['producers']],
        'licensors': [(lic['name'], lic['url']) for lic in anime_data['licensors']],
        'studios': [(stu['name'], stu['url']) for stu in anime_data['studios']],
        'genres': [(genre['name'], genre['url']) for genre in anime_data['genres']],
        'demographics': [(demo['name'], demo['url']) for demo in anime_data['demographics']],
        'synopsis': anime_data['synopsis'],
    })
    animes[0]['later'] = compare(AnimeWatchLater.objects, animes[0]['mal_id'], 'later', user)
    animes[0]['like'] = compare(Liked.objects, f'{animes[0]["mal_id"]}{animes[0]["type"]}', 'like', user)
    return animes


def get_schedule():
    anime_lst = []
    r = requests.get(f'https://api.jikan.moe/v4/schedules?filter={date.today().strftime("%A").lower()}&limit=25'
                     f'&kids=false')
    for anime_data in r.json()['data']:
        anime_lst.append({
            'status': r.status_code,
            'exceptions': r,
            'type': 'anime',
            'like': False,
            'later': False,
            'mal_id': anime_data['mal_id'],
            'img': anime_data['images']['webp']['large_image_url'],
            'default_title': anime_data['title'],
            'english_title': anime_data['title_english'],
            'episode': anime_data['episodes'],
            'ongoing': anime_data['airing'],
            'score': anime_data['score'],
        })
    return anime_lst


def recommendations_anime(user):
    anime_lst = []
    seen_ids = set()  # Set to store seen mal_ids

    request = requests.get('https://api.jikan.moe/v4/recommendations/anime')
    data = request.json()['data']

    for s in data:
        for anime_data in s['entry']:
            mal_id = anime_data['mal_id']
            if mal_id not in seen_ids:  # Check if mal_id is not seen before
                anime_lst.append({
                    'status': request.status_code,
                    'exceptions': request,
                    'mal_id': mal_id,
                    'type': 'anime',
                    'like': False,
                    'later': False,
                    'img': anime_data['images']['webp']['large_image_url'],
                    'default_title': anime_data['title'][0:50] + '...' if len(anime_data['title']) > 50 else anime_data[
                        'title']
                })
                seen_ids.add(mal_id)  # Add mal_id to seen_ids set
    compare_many(AnimeWatchLater.objects, anime_lst, 'later', user)
    compare_many(Liked.objects, anime_lst, 'like', user)
    return anime_lst


def manga_list(manga='', page=1, types='', status='', genres='', min_score='', max_score='', user=None):
    if manga:
        r = requests.get(f'https://api.jikan.moe/v4/manga?q={manga}')
    else:
        r = requests.get(f'https://api.jikan.moe/v4/manga?q='
                         f'{manga}&status={status}&page={page}&type={types}&genres={genres}&min_score={min_score}'
                         f'&max_score={max_score}&order_by=mal_id&sort=asc')
        # make top manga and anime view with filter
    mangas = []
    page_data = []
    seen_ids = set()
    for manga_data in r.json()['data']:
        mal_id = manga_data['mal_id']
        if mal_id not in seen_ids:
            mangas.append({
                'status': r.status_code,
                'exceptions': r,
                'type': 'manga',
                'like': False,
                'later': False,
                'mal_id': manga_data['mal_id'],
                'img': manga_data['images']['webp']['large_image_url'],
                'default_title': manga_data['title'],
                'english_title': manga_data['title_english'],
                'chapters': manga_data['chapters'],  # manga chapters
                'ongoing': manga_data['status'],
                'score': manga_data['score']
            })
            seen_ids.add(mal_id)
    page_data.append({'last_page': r.json()['pagination']['last_visible_page'],
                      'next_page': r.json()['pagination']['has_next_page']})
    compare_many(MangaWatchLater.objects, mangas, 'later', user)
    compare_many(Liked.objects, mangas, 'like', user)
    return mangas, page_data


def top_manga(page=1, types='', filters='', user=None):
    r = requests.get(f'https://api.jikan.moe/v4/top/manga?page={page}&type={types}&filter={filters}')
    mangas = []
    page_data = []
    for manga_data in r.json()['data']:
        mangas.append({
            'status': r.status_code,
            'exceptions': r,
            'type': 'manga',
            'like': False,
            'later': False,
            'mal_id': manga_data['mal_id'],
            'img': manga_data['images']['webp']['large_image_url'],
            'default_title': manga_data['title'],
            'english_title': manga_data['title_english'],
            'chapters': manga_data['chapters'],  # manga chapters
            'ongoing': manga_data['status'],
            'score': manga_data['score']
        })
    page_data.append({'last_page': r.json()['pagination']['last_visible_page'],
                      'next_page': r.json()['pagination']['has_next_page']})
    compare_many(MangaWatchLater.objects, mangas, 'later', user)
    compare_many(Liked.objects, mangas, 'like', user)
    return mangas, page_data


def get_manga(mal_id, user):
    mangas = []
    request = requests.get(f'https://api.jikan.moe/v4/manga/{mal_id}/full')
    manga_data = request.json()['data']
    mangas.append({  # do more with manga and anime
        'status': request.status_code,
        'exceptions': request,
        'mal_id': manga_data['mal_id'],
        'url': manga_data['url'],
        'type': 'manga',
        'media_type': manga_data['type'],
        'like': False,
        'later': False,
        'img': manga_data['images']['webp']['large_image_url'],
        'default_title': manga_data['title'],
        'english_title': manga_data['title_english'],
        'japanese_title': manga_data['title_japanese'],
        'chapters': manga_data['chapters'],
        'volumes': manga_data['volumes'],
        'publishing': manga_data['status'],
        'ongoing': manga_data['publishing'],
        'from': manga_data['published']['prop']['from']['year'],
        'to': manga_data['published']['prop']['to']['year'],
        'score': manga_data['score'],
        'scored_by': manga_data['scored_by'],
        'rank': manga_data['rank'],
        'popularity': manga_data['popularity'],
        'favorites': manga_data['favorites'],
        'synopsis': manga_data['synopsis'],
        'titles': [(name['type'], name['title']) for name in manga_data['titles']],
        'authors': [(pro['name'], pro['url']) for pro in manga_data['authors']],
        'serializations': [(lic['name'], lic['url']) for lic in manga_data['serializations']],
        'themes': [(stu['name'], stu['url']) for stu in manga_data['themes']],
        'genres': [(genre['name'], genre['url']) for genre in manga_data['genres']],
        'demographics': [(demo['name'], demo['url']) for demo in manga_data['demographics']],
    })
    mangas[0]['later'] = compare(MangaWatchLater.objects, mangas[0]['mal_id'], 'later', user)
    mangas[0]['like'] = compare(Liked.objects, f'{mangas[0]["mal_id"]}{mangas[0]["type"]}', 'like', user)
    return mangas


def manga_random(user):
    mangas = []
    request = requests.get(f'https://api.jikan.moe/v4/random/manga')
    manga_data = request.json()['data']
    mangas.append({  # do more with manga and anime
        'status': request.status_code,
        'exceptions': request,
        'mal_id': manga_data['mal_id'],
        'url': manga_data['url'],
        'type': 'manga',
        'like': False,
        'later': False,
        'img': manga_data['images']['webp']['large_image_url'],
        'default_title': manga_data['title'],
        'english_title': manga_data['title_english'],
        'japanese_title': manga_data['title_japanese'],
        'chapters': manga_data['chapters'],
        'volumes': manga_data['volumes'],
        'publishing': manga_data['status'],
        'from': manga_data['published']['prop']['from']['year'],
        'to': manga_data['published']['prop']['to']['year'],
        'score': manga_data['score'],
        'scored_by': manga_data['scored_by'],
        'rank': manga_data['rank'],
        'popularity': manga_data['popularity'],
        'favorites': manga_data['favorites'],
        'synopsis': manga_data['synopsis'],
        'titles': [(name['type'], name['title']) for name in manga_data['titles']],
        'authors': [(pro['name'], pro['url']) for pro in manga_data['authors']],
        'serializations': [(lic['name'], lic['url']) for lic in manga_data['serializations']],
        'themes': [(stu['name'], stu['url']) for stu in manga_data['themes']],
        'genres': [(genre['name'], genre['url']) for genre in manga_data['genres']],
        'demographics': [(demo['name'], demo['url']) for demo in manga_data['demographics']],
    })
    mangas[0]['later'] = compare(MangaWatchLater.objects, mangas[0]['mal_id'], 'later', user)
    mangas[0]['like'] = compare(Liked.objects, f'{mangas[0]["mal_id"]}{mangas[0]["type"]}', 'like', user)
    return mangas


def recommendations_manga(user):
    manga_lst = []
    seen_ids = set()  # Set to store seen mal_ids

    request = requests.get('https://api.jikan.moe/v4/recommendations/manga')
    data = request.json()['data']

    for s in data:
        for manga_data in s['entry']:
            mal_id = manga_data['mal_id']
            if mal_id not in seen_ids:  # Check if mal_id is not seen before
                manga_lst.append({
                    'status': request.status_code,
                    'exceptions': request,
                    'mal_id': mal_id,
                    'type': 'manga',
                    'like': False,
                    'later': False,
                    'img': manga_data['images']['webp']['large_image_url'],
                    'default_title': manga_data['title'][0:50] + '...' if len(manga_data['title']) > 50 else manga_data[
                        'title']
                })
                seen_ids.add(mal_id)  # Add mal_id to seen_ids set
    compare_many(MangaWatchLater.objects, manga_lst, 'later', user)
    compare_many(Liked.objects, manga_lst, 'like', user)
    return manga_lst


def characters(mal_id, manga=True):
    character_data = []
    if manga:
        r = requests.get(f'https://api.jikan.moe/v4/manga/{mal_id}/characters').json()
    else:
        r = requests.get(f'https://api.jikan.moe/v4/anime/{mal_id}/characters').json()
    for data in r['data']:
        character_data.append({
            'mal_id': data['character']['mal_id'],
            'img': data['character']['images']['webp']['image_url'],
            'name': data['character']['name'],
            'role': data['role']
        })
    return character_data


def get_character(mal_id):
    data = []
    r = requests.get(f'https://api.jikan.moe/v4/characters/{mal_id}/full').json()['data']
    data.append({
        'mal_id': r['mal_id'],
        'url': r['url'],
        'img': r['images']['webp']['image_url'],
        'name': r['name'],
        'name_kanji': r['name_kanji'],
        'nicknames': [names for names in r['nicknames']],
        'about': r['about'],
        'manga': [{'role': manga['role'], 'mal_id': manga['manga']['mal_id'],
                   'img': manga['manga']['images']['webp']['image_url'],
                   'title': manga['manga']['title'][:50] + '...' if len(manga['manga']['title'][:50]) > 50 else
                   manga['manga']['title'][:50]} for manga in r['manga']],
        'anime': [{'role': anime['role'], 'mal_id': anime['anime']['mal_id'],
                   'img': anime['anime']['images']['webp']['image_url'],
                   'title': anime['anime']['title'][:50] + '...' if len(anime['anime']['title'][:50]) > 50 else
                   anime['anime']['title'][:50]} for anime in r['anime']],
        'voices': [{'mal_id': voice['person']['mal_id'],
                    'img': voice['person']['images']['jpg']['image_url'],
                    'title': voice['person']['name'], 'language': voice['language']} for voice in r['voices']]
    })
    return data


def get_person(mal_id):
    data = []
    r = requests.get(f'https://api.jikan.moe/v4/people/{mal_id}/full').json()['data']
    data.append({
        'mal_id': r['mal_id'],
        'url': r['url'],
        'website_url': r['website_url'],
        'img': r['images']['jpg']['image_url'],
        'name': r['name'],
        'given_name': r['given_name'],
        'family_name': r['family_name'],
        'alternate_names': r['alternate_names'],
        'birthday': r['birthday'].split('T')[0],
        'about': r['about'],
        'anime': [{'position': anime['position'], 'mal_id': anime['anime']['mal_id'],
                   'img': anime['anime']['images']['webp']['image_url'], 'title': anime['anime']['title']}
                  for anime in r['anime']],
        'manga': [{'position': manga['position'], 'mal_id': manga['manga']['mal_id'],
                   'img': manga['manga']['images']['webp']['image_url'], 'title': manga['manga']['title']}
                  for manga in r['manga']],
        'voices': [{'role': voice['role'], 'mal_id': voice['anime']['mal_id'],
                    'img': voice['anime']['images']['webp']['image_url'], 'title': voice['anime']['title'],
                    'character_id': voice['character']['mal_id'],
                    'character_img': voice['character']['images']['jpg']['image_url'],
                    'name': voice['character']['name']} for voice in r['voices']],
    })
    return data


def compare(obj, mal_id, status, user):
    if status == 'later':
        if user:
            value = obj.filter(mal_id=mal_id, user=user).exists()
        else:
            value = obj.filter(mal_id=mal_id).exists()
        if value:
            return True
        else:
            return False
    else:
        if user:
            value = obj.filter(id=mal_id, user=user).exists()
        else:
            value = obj.filter(id=mal_id).exists()
        if value:
            return True
        else:
            return False


def compare_obj(obj1, obj2, update):
    model_1 = obj1
    model_2 = set(obj2.values_list('mal_id', 'type'))
    if update == 'like':
        for instance in model_1:
            if (instance.mal_id, instance.type) in model_2:
                instance.like = True
                instance.later = True
                instance.save()
        return model_1
    elif update == 'later':
        for instance in model_1:
            if (instance.mal_id, instance.type) in model_2:
                instance.later = True
                instance.like = True
                instance.save()
        return model_1


def genres(types):
    r = requests.get(f'https://api.jikan.moe/v4/genres/{types}').json()
    for data in r['data']:
        if types == 'anime':
            media_genre = AnimeGenres(
                mal_id=data['mal_id'],
                name=data['name'],
                url=data['url'],
                count=data['count']
            )
            media_genre.save()
            print('saved anime')
        else:
            media_genre = MangaGenres(
                mal_id=data['mal_id'],
                name=data['name'],
                url=data['url'],
                count=data['count']
            )
            media_genre.save()
            print('saved manga')


def compare_many(obj, lst, icon, user):
    if icon == 'later':
        for items in lst:
            if user:
                value = obj.filter(mal_id=items['mal_id'], user=user).exists()
            else:
                value = obj.filter(mal_id=items['mal_id']).exists()
            items[icon] = value
    else:
        for items in lst:
            value = obj.filter(id=f'{items["mal_id"]}{items["type"]}')
            items[icon] = value


def get_statistics(mal_id, manga=True):
    response = requests.get(
        f'https://api.jikan.moe/v4/manga/{mal_id}/statistics' if manga else f'https://api.jikan.moe/v4/anime/{mal_id}/statistics').json()
    data = response['data']
    return {
        'viewing': data['reading' if manga else 'watching'],
        'completed': data['completed'],
        'on_hold': data['on_hold'],
        'dropped': data['dropped'],
        'planing': data['plan_to_read' if manga else 'plan_to_watch']
    }


def get_more_info(mal_id, manga=True):
    r = requests.get(
        f'https://api.jikan.moe/v4/manga/{mal_id}/moreinfo' if manga else f'https://api.jikan.moe/v4/anime/{mal_id}/moreinfo').json()
    return r['data']['moreinfo']


anime_genres = list(names for names in AnimeGenres.objects.values('name'))

manga_genres = list(names for names in MangaGenres.objects.values('name'))
MANGA_FILTER_OPTIONS = [  # order everything by score
    {'name': 'type', 'options': ['manga', 'novel', 'light novel', 'oneshot', 'doujin', 'manhwa', 'manhua']},
    {'name': 'score', 'options': ['best', 'worst']},
    {'name': 'status', 'options': ['publishing', 'complete', 'hiatus', 'discontinued', 'upcoming']},
    {'name': 'genres', 'options': manga_genres},
]

TOP_MANGA_FILTER_OPTIONS = [  # order everything by score
    {'name': 'type', 'options': ['manga', 'novel', 'light novel', 'oneshot', 'doujin', 'manhwa', 'manhua']},
    {'name': 'filter', 'options': ['publishing', 'upcoming', 'bypopularity', 'favorite']}
]
WATCH_LATER_MANGA_FILTER_OPTIONS = [  # order everything by score
    {'name': 'type', 'options': ['manga', 'novel', 'light novel', 'oneshot', 'doujin', 'manhwa', 'manhua']},
    {'name': 'score', 'options': ['best', 'worst']},
    {'name': 'status', 'options': ['publishing', 'finished', 'hiatus', 'discontinued', 'upcoming']},
    {'name': 'genres', 'options': manga_genres},
]
ANIME_FILTER_OPTIONS = [
    {'name': 'type', 'options': ['tv', 'movie', 'ova', 'special', 'ona', 'music', 'cm', 'pv', 'tv_special']},
    {'name': 'score', 'options': ['best', 'worst']},
    {'name': 'status', 'options': ['airing', 'complete', 'upcoming']},
    {'name': 'rating', 'options': ['g', 'pg', 'pg13', 'r17', 'r', 'rx']},
    {'name': 'genres', 'options': anime_genres},
]
TOP_ANIME_FILTER_OPTIONS = [
    {'name': 'type', 'options': ['tv', 'movie', 'ova', 'special', 'ona', 'music', 'cm', 'pv', 'tv_special']},
    {'name': 'filter', 'options': ['airing', 'upcoming', 'bypopularity', 'favorite']},
    {'name': 'rating', 'options': ['g', 'pg', 'pg13', 'r17', 'r', 'rx']},
]
WATCH_LATER_ANIME_FILTER_OPTIONS = [
    {'name': 'type', 'options': ['tv', 'movie', 'ova', 'special', 'ona', 'music', 'cm', 'pv', 'tv_special']},
    {'name': 'score', 'options': ['best', 'worst']},
    {'name': 'status', 'options': ['currently airing', 'finished airing', 'upcoming']},
    {'name': 'rating', 'options': ['g', 'pg', 'pg13', 'r-17', 'r', 'rx']},
    {'name': 'genres', 'options': anime_genres},
]

# Combine the lists


combined_genres = []
for genre in anime_genres + manga_genres:
    if genre not in combined_genres:
        combined_genres.append(genre)
ALL_FILTER_OPTIONS = [
    {'name': 'type', 'options': ['tv', 'movie', 'ova', 'special', 'ona', 'music', 'cm', 'pv', 'tv_special',
                                 'manga', 'novel', 'light novel', 'oneshot', 'doujin', 'manhwa', 'manhua']},
    {'name': 'status', 'options': ['airing', 'upcoming', 'bypopularity', 'favorite',
                                   'publishing', 'complete', 'hiatus', 'discontinued', 'favorite']},
    {'name': 'score', 'options': ['best', 'worst']},
    {'name': 'rating', 'options': ['g', 'pg', 'pg13', 'r17', 'r', 'rx']},
    {'name': 'genres', 'options': combined_genres},
]

# https://api.jikan.moe/v4/anime/{id}/statistics
# https://api.jikan.moe/v4/anime/{id}/moreinfo
# https://api.jikan.moe/v4/anime/{id}/recommendations
# https://api.jikan.moe/v4/anime/{id}/relations
# https://api.jikan.moe/v4/anime/{id}/videos
# https://api.jikan.moe/v4/anime/{id}/userupdates  don't know what I'll do with this
# https://api.jikan.moe/v4/anime/{id}/reviews  learn javascript in django in order to do this
# https://api.jikan.moe/v4/anime/{id}/themes
# https://api.jikan.moe/v4/anime/{id}/external
# https://api.jikan.moe/v4/anime/{id}/streaming
# https://api.jikan.moe/v4/top/anime
# https://api.jikan.moe/v4/top/manga
# https://api.jikan.moe/v4/manga?q={anime}&sfw
# https://api.jikan.moe/v4/anime?q={anime}&sfw
# https://api.jikan.moe/v4/random/anime
# https://api.jikan.moe/v4/random/manga
# https://api.jikan.moe/v4/random/characters
# https://api.jikan.moe/v4/recommendations/anime
# https://api.jikan.moe/v4/watch/episodes
# https://api.jikan.moe/v4/watch/episodes/popular
# https://api.jikan.moe/v4/watch/promos
# https://api.jikan.moe/v4/manga/{id}/reviews
