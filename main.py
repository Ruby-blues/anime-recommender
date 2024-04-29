from animelist.models import Liked, MangaWatchLater, AnimeWatchLater
from animelist.api.jikan import get_manga, get_anime
from django.shortcuts import get_object_or_404


def add_like(mal_id, status, user):
    response = f'{mal_id}{status}'
    if status == 'manga':
        if Liked.objects.filter(id=response).exists():
            manga_instance = Liked.objects.get(id=response)
            if manga_instance.user.filter(id=user.id).exists():
                manga_instance.user.remove(user)
                if manga_instance.user.count() == 0:
                    manga_instance.delete()
                return False
            else:
                manga_instance.user.add(user)
                return True
        else:
            data = get_manga(mal_id, user)[0]
            data['like'] = True
            instance = Liked(
                id=f'{mal_id}{status}',
                mal_id=data['mal_id'],
                default_title=data['default_title'],
                type=data['type'],
                english_title=data['english_title'],
                japanese_title=data['japanese_title'],
                titles=data['titles'],
                img=data['img'],
                url=data['url'],
                score=data['score'],
                scored_by=data['scored_by'],
                rank=data['rank'],
                start=data['from'],
                end=data['to'],
                like=data['like'],
                later=data['later'],
                chapters=data['chapters'],
                volumes=data['volumes'],
                status=data['publishing'],
                media_type=data['media_type'],  # here
                ongoing=data['ongoing'],
                genre=data['genres']
            )
            instance.save()
            instance.user.add(user)
            return True
    else:
        if Liked.objects.filter(id=response).exists():
            anime_instance = Liked.objects.get(id=response)
            if anime_instance.user.filter(id=user.id).exists():
                anime_instance.user.remove(user)
                if anime_instance.user.count() == 0:
                    anime_instance.delete()
                return False
            else:
                anime_instance.user.add(user)
                return True
        else:
            data = get_anime(mal_id, user)[0]
            data['like'] = True
            instance = Liked(
                id=f'{mal_id}{status}',
                mal_id=data['mal_id'],
                default_title=data['default_title'],
                type=data['type'],
                english_title=data['english_title'],
                japanese_title=data['japanese_title'],
                titles=data['titles'],
                img=data['img'],
                url=data['url'],
                score=data['score'],
                scored_by=data['scored_by'],
                rank=data['rank'],
                start=data['aired_from'],
                end=data['aired_to'],
                like=data['like'],
                later=data['later'],
                episodes=data['episode'],
                ongoing=data['ongoing'],
                status=data['airing'],  # here
                source=data['source'],
                rated=data['rated'],
                media_type=data['media_type'],
                genre=data['genres']
            )
            instance.save()
            instance.user.add(user)
            return True


def add_manga(mal_id, user):
    print('nigga')
    if MangaWatchLater.objects.filter(mal_id=mal_id).exists():
        manga_instance = MangaWatchLater.objects.get(mal_id=mal_id)
        if manga_instance.user.filter(id=user.id).exists():
            manga_instance.user.remove(user)
            if manga_instance.user.count() == 0:
                manga_instance.delete()
            return False
        else:
            manga_instance.user.add(user)
            return True
    else:
        print('new')
        data = get_manga(mal_id, user)[0]
        instance = MangaWatchLater(
            mal_id=data['mal_id'],
            default_title=data['default_title'],
            english_title=data['english_title'],
            japanese_title=data['japanese_title'],
            titles=data['titles'],
            img=data['img'],
            url=data['url'],
            chapters=data['chapters'],
            volumes=data['volumes'],
            publishing=data['publishing'],
            score=data['score'],
            scored_by=data['scored_by'],
            rank=data['rank'],
            start=data['from'],
            end=data['to'],
            synopsis=data['synopsis'],
            genre=data['genres'],
            demographics=data['demographics'],
            themes=data['themes'],
            like=data['like'],
            media_type=data['media_type'],
            ongoing=data['ongoing'],
        )
        instance.save()
        instance.user.add(user)
        return True


def add_anime(mal_id, user):
    if AnimeWatchLater.objects.filter(mal_id=mal_id).exists():
        anime_instance = AnimeWatchLater.objects.get(mal_id=mal_id)
        if anime_instance.user.filter(id=user.id).exists():
            anime_instance.user.remove(user)
            if anime_instance.user.count() == 0:
                # If no more users are associated, delete the anime instance
                anime_instance.delete()
            return False
        else:
            anime_instance.user.add(user)
            return True
    else:
        data = get_anime(mal_id, user)[0]
        instance = AnimeWatchLater(
            mal_id=data['mal_id'],
            default_title=data['default_title'],
            english_title=data['english_title'],
            japanese_title=data['japanese_title'],
            titles=data['titles'],
            img=data['img'],
            url=data['url'],
            episodes=data['episode'],
            ongoing=data['ongoing'],
            score=data['score'],
            scored_by=data['scored_by'],
            rank=data['rank'],
            start=data['aired_from'],
            end=data['aired_to'],
            synopsis=data['synopsis'],
            genre=data['genres'],
            demographics=data['demographics'],
            like=data['like'],
            status=data['airing'],
            source=data['source'],
            rated=data['rated'],
            media_type=data['media_type'],
        )
        instance.save()
        instance.user.add(user)
        return True
