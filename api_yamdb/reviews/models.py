import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


User = get_user_model()
day = datetime.date.today()


class Title(models.Model):
    """Модель произведения."""
    objects = models.Manager()
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
    genre = models.ManyToManyField(
        'Genre',
        default='Будет определено админом позже',
        related_name='genres'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default='Будет определено админом позже',
        related_name='categories'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Модель комментариев к ревью, которые могут оставлять пользователи."""
    objects = models.Manager()
    author = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    """Модель ревью к произведениям, которые могут оставлять пользователи."""
    SCORE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    objects = models.Manager()
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)

    class Meta:
        unique_together = ('author', 'title')
        ordering = ('id',)


class Category(models.Model):
    """Модель категорий произведений."""
    objects = models.Manager()
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.TextField(
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
