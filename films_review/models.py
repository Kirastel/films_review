import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from films_review.custom import constants


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    born_date = models.DateField(
        help_text='YYYY-MM-DD',
        validators=[MaxValueValidator(limit_value=datetime.date.today)]
    )
    country_born = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ['first_name', 'last_name', 'born_date']
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'


class Writer(models.Model):
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    born_date = models.DateField(
        help_text='YYYY-MM-DD',
        validators=[MaxValueValidator(limit_value=datetime.date.today)]
    )
    country_born = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ['first_name', 'last_name', 'born_date']
        verbose_name = 'Writer'
        verbose_name_plural = 'Writers'


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    born_date = models.DateField(
        help_text='YYYY-MM-DD',
        validators=[MaxValueValidator(limit_value=datetime.date.today)]
    )
    country_born = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ['first_name', 'last_name', 'born_date']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Film(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='title on the english language'
    )
    original_title = models.CharField(
        max_length=200,
        help_text='title on the original language'
    )
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField(help_text='YYYY-MM-DD')
    post_date = models.DateField(
        help_text='YYYY-MM-DD',
        auto_now_add=True,
        auto_now=False
    )
    description = models.TextField(max_length=1024)
    continuance = models.PositiveIntegerField(help_text='mins.')
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    writer = models.ManyToManyField(Writer)
    actor = models.ManyToManyField(Actor)
    small_img = models.ImageField(
        upload_to='film_img/',
        default='film_img/default.jpg')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title} {self.post_date}'

    def get_absolute_url(self):
        return reverse('films_review:film', kwargs={
            'pk': self.pk,
            'slug': self.slug
        })

    def is_released(self):
        """
        Return True if film is released
        """
        return self.release_date <= datetime.date.today()

    class Meta:
        unique_together = ['title', 'original_title', 'post_date']
        verbose_name = 'Film'
        verbose_name_plural = 'Films'


class FilmImage(models.Model):
    film = models.ForeignKey(
        Film,
        null=True,
        on_delete=models.CASCADE,
        related_name='IMAGE'
    )
    image = models.ImageField(
        upload_to='img/film_img/big/',
        default='img/film_img/big/default.jpg'
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Film image'
        verbose_name_plural = 'Film images'

    def __str__(self):
        return f'Фотографии {self.film}'


class Review(models.Model):
    title = models.CharField(max_length=60)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    text = models.TextField(max_length=8192)
    rating = models.IntegerField(choices=constants.RATINGS)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
