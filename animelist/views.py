import re

import requests
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from userprofile.models import User

from main import add_like, add_anime, add_manga
from .api.video_stream import *
from .api.jikan import anime_list, get_anime, manga_list, get_manga, anime_random, manga_random, \
    recommendations_anime, recommendations_manga, MANGA_FILTER_OPTIONS, get_more_info, \
    ANIME_FILTER_OPTIONS, top_anime, TOP_ANIME_FILTER_OPTIONS, top_manga, TOP_MANGA_FILTER_OPTIONS, get_schedule, \
    characters, get_character, get_person, compare_obj, ALL_FILTER_OPTIONS, WATCH_LATER_ANIME_FILTER_OPTIONS, \
    WATCH_LATER_MANGA_FILTER_OPTIONS, genres
from .models import MangaWatchLater, Liked, AnimeWatchLater, MangaGenres, AnimeGenres

dropdown = [('home', 'aurora'),
            ('manga', 'manga-page'),
            ('top anime', 'top-anime'),
            ('top manga', 'top-manga'),
            ('random anime', 'random-anime-page'),
            ('random manga', 'random-manga-page'),
            ('recommend anime', 'recommendations-anime-page'),
            ('recommend manga', 'recommendations-manga-page'),
            ]

def authenticated(user):
    if user.is_authenticated:
        return user
    else:
        return None


# fix issue with search page
class IndexView(View):
    def get(self, request):
        return self.render_index(request)

    def post(self, request):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                if status == 'later':
                    result = add_anime(response, authenticated(request.user))
                else:
                    result = add_like(response, 'anime', authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

        if request.POST.get('next') or request.POST.get('back'):
            try:
                page_number = int(request.POST.get('page_number'))
                if request.POST.get('next'):
                    page_number += 1
                else:
                    page_number -= 1
                return self.render_index(request, page_number)
            except Exception as e:
                print(e)

    def render_index(self, request, page_number=1):
        carousel_images = get_schedule()
        filters = ANIME_FILTER_OPTIONS
        anime_data = self.filter(request, page_number)
        animes = anime_data[0]
        pages = anime_data[1]
        return render(request, 'index.html', {'anime_api_data': animes, 'dropdown_items': dropdown,
                                              'pages': pages, 'page_number': page_number, 'filter_options': filters,
                                              'carousel_images': carousel_images})

    def filter(self, request, page_number, anime=''):
        try:
            genres = ''
            min_score = 1
            max_score = 10
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            scores = request.GET['score'] if list(request.GET.keys())[0] == 'score' else ''
            status = request.GET['status'] if list(request.GET.keys())[0] == 'status' else ''
            genre = request.GET['genres'] if list(request.GET.keys())[0] == 'genres' else ''
            rating = request.GET['rating'] if list(request.GET.keys())[0] == 'rating' else ''
            if genre:
                genres = AnimeGenres.objects.filter(name=genre).values('mal_id').get()['mal_id']
            if scores == 'best':
                min_score = 6
                max_score = 10
            elif scores == 'worst':
                min_score = 1
                max_score = 5.9

            return anime_list(anime=anime, page=page_number, types=types, status=status, genres=genres,
                              min_score=min_score, max_score=max_score, rating=rating, user=authenticated(request.user))
        except Exception as e:
            print(e)
            return anime_list(anime, page=page_number, user=authenticated(request.user))


class TopAnimeView(View):
    def get(self, request):
        return self.render_anime(request)

    def post(self, request):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                if status == 'later':
                    result = add_anime(response, authenticated(request.user))
                else:
                    result = add_like(response, 'anime', authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

        if request.POST.get('next') or request.POST.get('back'):
            try:
                page_number = int(request.POST.get('page_number'))
                if request.POST.get('next'):
                    page_number += 1
                else:
                    page_number -= 1
                return self.render_anime(request, page_number)
            except Exception as e:
                print(e)

    def render_anime(self, request, page_number=1):
        filters = TOP_ANIME_FILTER_OPTIONS
        anime_data = self.filter(request, page_number)
        animes = anime_data[0]
        pages = anime_data[1]
        return render(request, 'top_anime.html', {'anime_api_data': animes, 'dropdown_items': dropdown,
                                                  'pages': pages, 'page_number': page_number,
                                                  'filter_options': filters})

    def filter(self, request, page_number):
        try:
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            filters = request.GET['filter'] if list(request.GET.keys())[0] == 'filter' else ''
            rating = request.GET['rating'] if list(request.GET.keys())[0] == 'rating' else ''

            return top_anime(page=page_number, types=types, rating=rating, filters=filters, user=authenticated(request.user))
        except Exception as e:
            print(e)
            return top_anime(page=page_number, user=authenticated(request.user))


class RandomAnimeView(View):
    def get(self, request):
        animes = anime_random(authenticated(request.user))
        return render(request, 'random_anime.html', {'anime_api_data': animes})


class AnimeRecommendationsView(View):
    def get(self, request):
        animes = recommendations_anime(authenticated(request.user))
        return render(request, 'anime_recommendations.html', {'anime_api_data': animes, 'dropdown_items': dropdown})


class MangaRecommendationsView(View):
    def get(self, request):
        mangas = recommendations_manga(authenticated(request.user))
        return render(request, 'manga_recommendations.html', {'manga_api_data': mangas, 'dropdown_items': dropdown})


class MangaPageView(View):
    def get(self, request):
        return self.render_manga_page(request)

    def post(self, request):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                if status == 'later':
                    result = add_manga(response, authenticated(request.user))
                else:
                    result = add_like(response, 'manga', authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

        if request.POST.get('next') or request.POST.get('back'):
            try:
                page_number = int(request.POST.get('page_number'))
                if request.POST.get('next'):
                    page_number += 1
                else:
                    page_number -= 1
                return self.render_manga_page(request, page_number)
            except Exception as e:
                print(e)

    def render_manga_page(self, request, page_number=1):
        filters = MANGA_FILTER_OPTIONS
        manga_data = self.filter(request, page_number)
        mangas = manga_data[0]
        pages = manga_data[1]
        return render(request, 'manga_info_card.html', {'manga_api_data': mangas, 'dropdown_items': dropdown,
                                                        'pages': pages, 'page_number': page_number,
                                                        'filter_options': filters})

    def filter(self, request, page_number, manga=''):
        try:
            genres = ''
            min_score = 1
            max_score = 10
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            scores = request.GET['score'] if list(request.GET.keys())[0] == 'score' else ''
            status = request.GET['status'] if list(request.GET.keys())[0] == 'status' else ''
            genre = request.GET['genres'] if list(request.GET.keys())[0] == 'genres' else ''
            if genre:
                genres = MangaGenres.objects.filter(name=genre).values('mal_id').get()['mal_id']
            if scores == 'best':
                min_score = 6
                max_score = 10
            elif scores == 'worst':
                min_score = 1
                max_score = 5.9

            return manga_list(manga=manga, page=page_number, types=types, status=status, genres=genres,
                              min_score=min_score, max_score=max_score, user=authenticated(request.user))
        except Exception as e:
            print(e)
            return manga_list(manga=manga, page=page_number, user=authenticated(request.user))


class TopMangaView(View):
    def get(self, request):
        return self.render_manga(request)

    def post(self, request):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                if status == 'later':
                    result = add_manga(response, authenticated(request.user))
                else:
                    result = add_like(response, 'manga', authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

        if request.POST.get('next') or request.POST.get('back'):
            try:
                page_number = int(request.POST.get('page_number'))
                if request.POST.get('next'):
                    page_number += 1
                else:
                    page_number -= 1
                return self.render_manga(request, page_number)
            except Exception as e:
                print(e)

    def render_manga(self, request, page_number=1):
        filters = TOP_MANGA_FILTER_OPTIONS
        manga_data = self.filter(request, page_number)
        mangas = manga_data[0]
        pages = manga_data[1]
        return render(request, 'top_manga.html', {'manga_api_data': mangas, 'dropdown_items': dropdown,
                                                  'pages': pages, 'page_number': page_number,
                                                  'filter_options': filters})

    def filter(self, request, page_number):
        try:
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            filters = request.GET['filter'] if list(request.GET.keys())[0] == 'filter' else ''

            return top_manga(page=page_number, types=types, filters=filters, user=authenticated(request.user))
        except Exception as e:
            print(e)
            return top_manga(page=page_number, user=authenticated(request.user))


class RandomMangaView(View):
    def get(self, request):
        mangas = manga_random(authenticated(request.user))
        return render(request, 'random_manga.html', {'manga_api_data': mangas})


class MangaInfoPageView(View):
    def get(self, request, mal_id, name):
        mangas = get_manga(mal_id, authenticated(request.user))
        character = characters(mal_id)
        more_info = get_more_info(mal_id)  # maybe add a button to show more info
        return render(request, 'more_manga_info.html', {'manga_api_data': mangas, 'name': name,
                                                        'character_data': character, 'more_info': more_info})


class SearchAnimeView(View):
    def get(self, request):
        searched = request.GET.get('searched')
        media_type = request.GET.get('type')
        if media_type == 'anime':
            animes = anime_list(searched, user=authenticated(request.user))[0]
            if animes:
                try:
                    return render(request, 'searched_anime.html', {'searched': searched, 'anime_api_data': animes,
                                                                   'dropdown_items': dropdown,
                                                                   'media_type': media_type})
                except Exception as e:
                    print(e)
                    return render(request, 'error.html', {'error': e})
            else:
                return render(request, 'error.html', {'searched': searched})
        else:
            page_number = 1
            manga_data = manga_list(searched, page_number, authenticated(request.user))
            mangas = manga_data[0]
            pages = manga_data[1]
            if mangas:
                if request.POST.get('next'):
                    try:
                        page_number = int(request.POST.get('page_number')) + 1
                        manga_data = manga_list(manga=searched, page=page_number)
                        mangas = manga_data[0]
                        pages = manga_data[1]
                        return render(request, 'searched_anime.html',
                                      {'manga_api_data': mangas, 'dropdown_items': dropdown,
                                       'pages': pages, 'page_number': page_number})
                    except Exception as e:
                        return render(request, 'error.html', {'error': e})
                if request.POST.get('back'):
                    try:
                        page_number = int(request.POST.get('page_number')) - 1
                        manga_data = manga_list(manga=searched, page=page_number, user=authenticated(request.user))
                        mangas = manga_data[0]
                        pages = manga_data[1]
                        return render(request, 'searched_anime.html',
                                      {'manga_api_data': mangas, 'dropdown_items': dropdown,
                                       'pages': pages, 'page_number': page_number})
                    except Exception as e:
                        return render(request, 'error.html', {'error': e})
                try:
                    return render(request, 'searched_anime.html', {'searched': searched, 'manga_api_data': mangas,
                                                                   'dropdown_items': dropdown,
                                                                   'media_type': media_type, 'pages': pages,
                                                                   'page_number': page_number})
                except Exception as e:
                    print(e)
                    return render(request, 'error.html', {'error': e})
            else:
                return render(request, 'error.html', {'searched': searched})


class AnimeInfoPageView(View):
    def get(self, request, mal_id, name):
        animes = get_anime(mal_id, authenticated(request.user))
        character = characters(mal_id, False)
        more_info = get_more_info(mal_id, False)
        video = stream_video(animes[0].get('trailer'))
        return render(request, 'more_anime_info.html', {'anime_api_data': animes, 'name': name, 'video_url': video,
                                                        'character_data': character, 'more_info': more_info})


class CharacterView(View):
    def get(self, request, mal_id, name):
        character = get_character(mal_id)
        return render(request, 'more_character_info.html', {'character_data': character, 'name': name})


class PersonView(View):
    def get(self, request, mal_id, name):
        person = get_person(mal_id)
        return render(request, 'more_person_info.html', {'person_data': person, 'name': name})


class LikedView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, types):
        page = 1
        search = ''
        try:
            search = request.GET['searched']
        except Exception as e:
            print(e)
        try:
            page = request.GET['page']
        except Exception as e:
            print(e)
        likes = self.search(request, search, types)
        paginator = Paginator(likes, 25)
        page_obj = paginator.get_page(page)
        filter_options = self.genre_selector(types)
        return render(request, 'favorites.html', {'page_obj': page_obj, 'dropdown_items': dropdown, 'type': types,
                                                  'filter_options': filter_options})

    def post(self, request, types, *args):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                types = request.POST.get('type')
                if status == 'later':
                    if types == 'manga':
                        result = add_manga(response, authenticated(request.user))
                    else:
                        result = add_anime(response, authenticated(request.user))
                else:
                    result = add_like(response, types, authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

    def search(self, request, search, types):
        likes = self.filter(request, types, search)
        likes = compare_obj(likes, AnimeWatchLater.objects.all(), 'later')
        likes = compare_obj(likes, MangaWatchLater.objects.all(), 'later')
        return likes

    def filter(self, request, types, search):  # filter the rest
        like = Liked.objects.filter(user=authenticated(request.user)).order_by('-time')
        if types == 'all':
            like = like
        else:
            like = like.filter(type=types)
        if search:
            likes = like.filter(Q(default_title__icontains=search) | Q(english_title__icontains=search),
                                Q(japanese_title__icontains=search) | Q(titles__icontains=search))
        else:
            likes = like
        try:
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            scores = request.GET['score'] if list(request.GET.keys())[0] == 'score' else ''
            status = request.GET['status'] if list(request.GET.keys())[0] == 'status' else ''
            rated = request.GET['rating'] if list(request.GET.keys())[0] == 'rating' else ''
            genre = request.GET['genres'] if list(request.GET.keys())[0] == 'genres' else ''
            if types:
                likes = likes.filter(media_type__icontains=types)
            if scores:
                if scores == 'best':
                    likes = likes.filter(score__gte=6)
                if scores == 'worst':
                    likes = likes.filter(score__lte=5.9)
            if status:
                likes = likes.filter(status__icontains=status)
            if genre:
                likes = likes.filter(genre__icontains=genre)
            if rated:
                likes = likes.filter(rated__icontains=rated)
            return likes
        except Exception as e:
            return likes

    def genre_selector(self, types):
        if types == 'all':
            genres = ALL_FILTER_OPTIONS
        elif types == 'anime':
            genres = ANIME_FILTER_OPTIONS
        else:
            genres = MANGA_FILTER_OPTIONS
        return genres


class LaterAnimeView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        page = 1
        search = ''
        try:
            page = request.GET['page']
        except Exception as e:
            print(e)
        try:
            search = request.GET['searched']
        except Exception as e:
            print(e)
        anime = self.search(request, search)
        paginator = Paginator(anime, 25)
        page_obj = paginator.get_page(page)
        anime_genres = WATCH_LATER_ANIME_FILTER_OPTIONS
        return render(request, 'watch_later_anime.html', {'page_obj': page_obj, 'dropdown_items': dropdown,
                                                          'filter_options': anime_genres, 'type': 'anime'})

    def post(self, request):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                types = request.POST.get('type')
                if status == 'later':
                    result = add_anime(response, authenticated(request.user))
                else:
                    result = add_like(response, types, authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

    def search(self, request, search):
        animes = self.filter(request, search)

        animes = compare_obj(animes, Liked.objects.all(), 'like')

        return animes

    def filter(self, request, search):  # filter the rest
        anime = AnimeWatchLater.objects.filter(user=authenticated(request.user)).order_by('-time')
        if search:
            animes = anime.filter(Q(default_title__icontains=search) | Q(english_title__icontains=search),
                                  Q(japanese_title__icontains=search) | Q(titles__icontains=search))
        else:
            animes = anime
        try:
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            scores = request.GET['score'] if list(request.GET.keys())[0] == 'score' else ''
            status = request.GET['status'] if list(request.GET.keys())[0] == 'status' else ''
            rated = request.GET['rating'] if list(request.GET.keys())[0] == 'rating' else ''
            genre = request.GET['genres'] if list(request.GET.keys())[0] == 'genres' else ''
            if types:
                animes = animes.filter(media_type__icontains=types)
            if scores:
                if scores == 'best':
                    animes = animes.filter(score__gte=6)
                if scores == 'worst':
                    animes = animes.filter(score__lte=5.9)
            if status:
                animes = animes.filter(status__icontains=status)
            if genre:
                animes = animes.filter(genre__icontains=genre)
            if rated:
                animes = animes.filter(rated__icontains=rated)
            return animes
        except Exception as e:
            return animes


class LaterMangaView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        page = 1
        search = ''
        try:
            page = request.GET['page']
        except Exception as e:
            print(e)
        try:
            search = request.GET['searched']
        except Exception as e:
            print(e)
        user = User
        manga = self.search(request, search)
        paginator = Paginator(manga, 25)
        page_obj = paginator.get_page(page)
        manga_genres = WATCH_LATER_MANGA_FILTER_OPTIONS
        return render(request, 'watch_later_manga.html', {'page_obj': page_obj, 'type': 'manga',
                                                          'dropdown_items': dropdown, 'filter_options': manga_genres,
                                                          'user': user})

    def post(self, request, *args):
        status = request.POST.get('status')
        if status in ['later', 'like']:
            try:
                response = request.POST.get('mal_id')
                types = request.POST.get('type')
                if status == 'later':
                    result = add_manga(response, authenticated(request.user))
                else:
                    result = add_like(response, types, authenticated(request.user))
                return JsonResponse({status: result})
            except Exception as e:
                print(e)

    def search(self, request, search):
        mangas = self.filter(request, search)
        mangas = compare_obj(mangas, Liked.objects.all(), 'like')
        return mangas

    def filter(self, request, search):  # filter the rest
        manga = MangaWatchLater.objects.filter(user=authenticated(request.user)).order_by('-time')
        if search:
            mangas = manga.filter(Q(default_title__icontains=search) | Q(english_title__icontains=search),
                                  Q(japanese_title__icontains=search) | Q(titles__icontains=search))
        else:
            mangas = manga
        try:
            types = request.GET['type'] if list(request.GET.keys())[0] == 'type' else ''
            scores = request.GET['score'] if list(request.GET.keys())[0] == 'score' else ''
            status = request.GET['status'] if list(request.GET.keys())[0] == 'status' else ''
            genre = request.GET['genres'] if list(request.GET.keys())[0] == 'genres' else ''
            if types:
                mangas = mangas.filter(media_type__icontains=types)
            if scores:
                if scores == 'best':
                    mangas = mangas.filter(score__gte=6)
                if scores == 'worst':
                    mangas = mangas.filter(score__lte=5.9)
            if status:
                mangas = mangas.filter(publishing__icontains=status)
            if genre:
                mangas = mangas.filter(genre__icontains=genre)
            return mangas
        except Exception as e:
            return mangas
