from django.db import models
from django.utils import timezone
from userprofile.models import User


class AnimeWatchLater(models.Model):
    mal_id = models.IntegerField(unique=True, primary_key=True)
    user = models.ManyToManyField(User, related_name='later_anime')
    type = models.CharField(max_length=50, default='anime')
    default_title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255, blank=True, null=True)
    japanese_title = models.CharField(max_length=255, blank=True, null=True)
    titles = models.JSONField(default=list)
    img = models.CharField(max_length=2085)
    url = models.CharField(max_length=2085)
    episodes = models.IntegerField(blank=True, null=True)
    ongoing = models.BooleanField(default=False)
    status = models.CharField(max_length=150, blank=True, null=True)
    media_type = models.CharField(max_length=60, blank=True, null=True)
    rated = models.CharField(max_length=10, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    start = models.CharField(max_length=20, null=True)
    end = models.CharField(max_length=20, null=True)
    synopsis = models.TextField(max_length=3000, null=True, blank=True)
    genre = models.JSONField(default=list)
    demographics = models.JSONField(default=list)
    like = models.BooleanField(default=False)
    later = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ['-time']


class MangaWatchLater(models.Model):
    mal_id = models.IntegerField(unique=True, primary_key=True)
    user = models.ManyToManyField(User, related_name='later_manga')
    auther = models.JSONField(default=list)
    type = models.CharField(max_length=50, default='manga')
    default_title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255, blank=True, null=True)
    japanese_title = models.CharField(max_length=255, blank=True, null=True)
    titles = models.JSONField(default=list)
    img = models.CharField(max_length=2085)
    url = models.CharField(max_length=2085)
    chapters = models.IntegerField(blank=True, null=True)
    volumes = models.IntegerField(blank=True, null=True)
    publishing = models.CharField(max_length=150, blank=True, null=True)
    ongoing = models.BooleanField()
    media_type = models.CharField(max_length=60, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    start = models.CharField(max_length=20, null=True, blank=True)
    end = models.CharField(max_length=20, null=True, blank=True)
    synopsis = models.TextField(max_length=3000, null=True, blank=True)
    genre = models.JSONField(default=list)
    demographics = models.JSONField(default=list)
    themes = models.JSONField(default=list)
    like = models.BooleanField(default=False)
    later = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ['-time']


class Liked(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ManyToManyField(User, related_name='liked')
    mal_id = models.IntegerField()
    default_title = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    media_type = models.CharField(max_length=150, blank=True, null=True)
    english_title = models.CharField(max_length=255, blank=True, null=True)
    japanese_title = models.CharField(max_length=255, blank=True, null=True)
    titles = models.JSONField(default=list)
    img = models.CharField(max_length=2085)
    url = models.CharField(max_length=2085)
    episodes = models.IntegerField(null=True, blank=True)
    ongoing = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    rated = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    chapters = models.IntegerField(blank=True, null=True)
    volumes = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    scored_by = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    genre = models.JSONField(default=list)
    start = models.CharField(max_length=20, null=True, blank=True)
    end = models.CharField(max_length=20, null=True, blank=True)
    like = models.BooleanField(default=True)
    later = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ['-time']


class MangaGenres(models.Model):
    mal_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    url = models.URLField(max_length=120, unique=True)
    count = models.IntegerField(default=0)


class AnimeGenres(models.Model):
    mal_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    url = models.URLField(max_length=120, unique=True)
    count = models.IntegerField(default=0)





