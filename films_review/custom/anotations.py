from films_review.models import Film, Director, Writer, Actor
from django.db.models import Avg, Count, Value
from django.db.models.functions import Coalesce, Concat


def get_annotated_films(queryset):
    num_reviews = Count('review__id')
    avg_rating = Coalesce(Avg('review__rating'), float(0))
    annotated_films_queryset = queryset.annotate(
        num_reviews=num_reviews,
        avg_rating=avg_rating
    )
    return annotated_films_queryset


def get_annotated_directors(directors_queryset):
    director_full_name = Concat('first_name', Value(' '), 'patronymic', Value(' '), 'last_name')
    director_short_name = Concat('first_name', Value(' '), 'last_name')
    annotated_director_queryset = directors_queryset.annotate(
        full_name=director_full_name,
        short_name=director_short_name
    )
    return annotated_director_queryset


def get_annotated_actors(actors_queryset):
    actor_full_name = Concat('first_name', Value(' '), 'patronymic', Value(' '), 'last_name')
    actor_short_name = Concat('first_name', Value(' '), 'last_name')
    annotated_actors_queryset = actors_queryset.annotate(
        full_name=actor_full_name,
        short_name=actor_short_name
    )
    1
    return annotated_actors_queryset


def get_annotated_writers(writers_queryset):
    writer_full_name = Concat('first_name', Value(' '), 'patronymic', Value(' '), 'last_name')
    writer_short_name = Concat('first_name', Value(' '), 'last_name')
    annotated_writers_queryset = writers_queryset.annotate(
        full_name=writer_full_name,
        short_name=writer_short_name
    )
    return annotated_writers_queryset


annotated_films = get_annotated_films(Film.objects.filter(is_active=True))
annotated_directors = get_annotated_directors(Director.objects.all())
annotated_writers = get_annotated_writers(Writer.objects.all())
annotated_actors = get_annotated_actors(Actor.objects.all())
