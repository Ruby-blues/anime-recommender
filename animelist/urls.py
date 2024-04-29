from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='aurora'),
    path('top/anime/', views.TopAnimeView.as_view(), name='top-anime'),
    path('searched', views.SearchAnimeView.as_view(), name='searched-media'),
    path('anime_info/<int:mal_id>/<str:name>/', views.AnimeInfoPageView.as_view(), name='anime-info-page'),
    path('random_anime/', views.RandomAnimeView.as_view(), name='random-anime-page'),
    path('recommendations_anime/', views.AnimeRecommendationsView.as_view(), name='recommendations-anime-page'),

    path('manga/', views.MangaPageView.as_view(), name='manga-page'),
    path('top/manga/', views.TopMangaView.as_view(), name='top-manga'),
    path('random_manga/', views.RandomMangaView.as_view(), name='random-manga-page'),
    path('manga_info/<int:mal_id>/<str:name>/', views.MangaInfoPageView.as_view(), name='manga-info-page'),
    path('recommendations_manga/', views.MangaRecommendationsView.as_view(), name='recommendations-manga-page'),

    path('character/<int:mal_id>/<str:name>/', views.CharacterView.as_view(), name='character-info'),
    path('person/<int:mal_id>/<str:name>/', views.PersonView.as_view(), name='person-info-page'),

    path('liked/<str:types>', views.LikedView.as_view(), name='liked-page'),
    path('watch_later/anime', views.LaterAnimeView.as_view(), name='later-anime-page'),
    path('watch_later/manga', views.LaterMangaView.as_view(), name='later-manga-page'),

]
