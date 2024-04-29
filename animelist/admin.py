from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.
from .models import MangaGenres, AnimeGenres, Liked, MangaWatchLater, AnimeWatchLater


class GenreConfig(ModelAdmin):
    search_fields = ('name', 'mal_id')
    ordering = ('-mal_id',)
    list_display = ('mal_id', 'name', 'count')
    fieldsets = (
        ('Genres', {'fields': ('mal_id', 'name', 'count')}),
        ('urls', {'fields': ('url',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mal_id', 'name', 'count', 'url')}
         ),
    )


class Config(ModelAdmin):
    search_fields = ('default_title', 'english_title')
    ordering = ('-time',)
    list_display = ('mal_id', 'default_title', 'media_type', 'type')


admin.site.register(MangaGenres, GenreConfig)
admin.site.register(AnimeGenres, GenreConfig)
admin.site.register(Liked, Config)
admin.site.register(MangaWatchLater, Config)
admin.site.register(AnimeWatchLater, Config)
