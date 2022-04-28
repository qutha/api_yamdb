import datetime

from django.db import models
from django.core.validators import MaxValueValidator

day = datetime.date.today()


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.TextField(
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=(MaxValueValidator(day.year),)
    )
    rating = models.FloatField(
        verbose_name='Рейтинг произведения',
        blank=True,
        null=True)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_DEFAULT,
        default='Будет определено админом позже',
        related_name='genres'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_DEFAULT,
        default='Будет определено админом позже',
        related_name='categories'
    )

    def __str__(self):
        return self.name
