# Generated by Django 5.0.3 on 2024-04-26 07:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AnimeGenres",
            fields=[
                (
                    "mal_id",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                ("name", models.CharField(max_length=120, unique=True)),
                ("url", models.URLField(max_length=120, unique=True)),
                ("count", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="AnimeWatchLater",
            fields=[
                (
                    "mal_id",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                ("type", models.CharField(default="anime", max_length=50)),
                ("default_title", models.CharField(max_length=255)),
                (
                    "english_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "japanese_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("titles", models.JSONField(default=list)),
                ("img", models.CharField(max_length=2085)),
                ("url", models.CharField(max_length=2085)),
                ("episodes", models.IntegerField(blank=True, null=True)),
                ("ongoing", models.BooleanField(default=False)),
                ("status", models.CharField(blank=True, max_length=150, null=True)),
                ("media_type", models.CharField(blank=True, max_length=60, null=True)),
                ("rated", models.CharField(blank=True, max_length=10, null=True)),
                ("score", models.FloatField(blank=True, null=True)),
                ("source", models.CharField(blank=True, max_length=20, null=True)),
                ("scored_by", models.IntegerField(blank=True, null=True)),
                ("rank", models.IntegerField(blank=True, null=True)),
                ("start", models.CharField(max_length=20, null=True)),
                ("end", models.CharField(max_length=20, null=True)),
                ("synopsis", models.TextField(blank=True, max_length=3000, null=True)),
                ("genre", models.JSONField(default=list)),
                ("demographics", models.JSONField(default=list)),
                ("like", models.BooleanField(default=False)),
                ("later", models.BooleanField(default=True)),
                ("time", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Liked",
            fields=[
                (
                    "id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("mal_id", models.IntegerField()),
                ("default_title", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=50)),
                ("media_type", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "english_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "japanese_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("titles", models.JSONField(default=list)),
                ("img", models.CharField(max_length=2085)),
                ("url", models.CharField(max_length=2085)),
                ("episodes", models.IntegerField(blank=True, null=True)),
                ("ongoing", models.BooleanField(blank=True, default=False, null=True)),
                ("status", models.CharField(blank=True, max_length=150, null=True)),
                ("rated", models.CharField(blank=True, max_length=10, null=True)),
                ("source", models.CharField(blank=True, max_length=20, null=True)),
                ("chapters", models.IntegerField(blank=True, null=True)),
                ("volumes", models.IntegerField(blank=True, null=True)),
                ("score", models.FloatField(blank=True, null=True)),
                ("scored_by", models.IntegerField(blank=True, null=True)),
                ("rank", models.IntegerField(blank=True, null=True)),
                ("genre", models.JSONField(default=list)),
                ("start", models.CharField(blank=True, max_length=20, null=True)),
                ("end", models.CharField(blank=True, max_length=20, null=True)),
                ("like", models.BooleanField(default=True)),
                ("later", models.BooleanField(default=False)),
                ("time", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="MangaGenres",
            fields=[
                (
                    "mal_id",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                ("name", models.CharField(max_length=120, unique=True)),
                ("url", models.URLField(max_length=120, unique=True)),
                ("count", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="MangaWatchLater",
            fields=[
                (
                    "mal_id",
                    models.IntegerField(primary_key=True, serialize=False, unique=True),
                ),
                ("auther", models.JSONField(default=list)),
                ("type", models.CharField(default="manga", max_length=50)),
                ("default_title", models.CharField(max_length=255)),
                (
                    "english_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "japanese_title",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("titles", models.JSONField(default=list)),
                ("img", models.CharField(max_length=2085)),
                ("url", models.CharField(max_length=2085)),
                ("chapters", models.IntegerField(blank=True, null=True)),
                ("volumes", models.IntegerField(blank=True, null=True)),
                ("publishing", models.CharField(blank=True, max_length=150, null=True)),
                ("ongoing", models.BooleanField()),
                ("media_type", models.CharField(blank=True, max_length=60, null=True)),
                ("score", models.FloatField(blank=True, null=True)),
                ("scored_by", models.IntegerField(blank=True, null=True)),
                ("rank", models.IntegerField(blank=True, null=True)),
                ("start", models.CharField(blank=True, max_length=20, null=True)),
                ("end", models.CharField(blank=True, max_length=20, null=True)),
                ("synopsis", models.TextField(blank=True, max_length=3000, null=True)),
                ("genre", models.JSONField(default=list)),
                ("demographics", models.JSONField(default=list)),
                ("themes", models.JSONField(default=list)),
                ("like", models.BooleanField(default=False)),
                ("later", models.BooleanField(default=True)),
                ("time", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
