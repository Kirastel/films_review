from django.contrib import admin
from . import models


class FilmImageInline(admin.TabularInline):
    model = models.FilmImage
    extra = 4


class DirectorInLine(admin.TabularInline):
    model = models.Film.director.through
    extra = 1


class WriterInLine(admin.TabularInline):
    model = models.Film.writer.through
    extra = 1


class ActorInLine(admin.TabularInline):
    model = models.Film.actor.through
    extra = 1


class GenreInLine(admin.TabularInline):
    model = models.Film.genres.through
    extra = 1


@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Film._meta.fields]
    inlines = [
        FilmImageInline,
        DirectorInLine,
        WriterInLine,
        ActorInLine,
        GenreInLine,
    ]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(models.Genre)
admin.site.register(models.Country)
admin.site.register(models.Director)
admin.site.register(models.Writer)
admin.site.register(models.Actor)
