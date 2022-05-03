# from django.db import models
# from django.contrib.auth import get_user_model
#
# import datetime
#
# from django.core.validators import MaxValueValidator
#
# day = datetime.date.today()
#
# User = get_user_model()
#
#
# class Comment(models.Model):
#     objects = models.Manager()
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='comments'
#     )
#     review = models.ForeignKey(
#         'Review', on_delete=models.CASCADE, related_name='comments'
#     )
#     text = models.TextField()
#     pub_date = models.DateTimeField(
#         'Дата добавления', auto_now_add=True, db_index=True
#     )
#
#
# class Review(models.Model):
#     SCORE_CHOICES = (
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#         (6, '6'),
#         (7, '7'),
#         (8, '8'),
#         (9, '9'),
#         (10, '10'),
#     )
#     objects = models.Manager()
#     text = models.TextField()
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='posts'
#     )
#     composition = models.ForeignKey(
#         'Title', on_delete=models.CASCADE,
#     )
#     score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
#
#
# class Categories(models.Model):
#     name = models.CharField(
#         max_length=256,
#         unique=True
#     )
#     slug = models.SlugField(
#         max_length=50,
#         unique=True
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class Genres(models.Model):
#     name = models.TextField(
#         unique=True
#     )
#     slug = models.SlugField(
#         unique=True
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class Titles(models.Model):
#     name = models.CharField(
#         max_length=256,
#         verbose_name='Название'
#     )
#     description = models.TextField(
#         null=True,
#         blank=True,
#         verbose_name='Описание'
#     )
#     year = models.PositiveIntegerField(
#         verbose_name='Год выпуска',
#         validators=(MaxValueValidator(day.year),)
#     )
#     rating = models.FloatField(
#         verbose_name='Рейтинг произведения',
#         blank=True,
#         null=True)
#     genre = models.ForeignKey(
#         Genres,
#         on_delete=models.SET_DEFAULT,
#         default='Будет определено админом позже',
#         related_name='genres'
#     )
#     category = models.ForeignKey(
#         Categories,
#         on_delete=models.SET_DEFAULT,
#         default='Будет определено админом позже',
#         related_name='categories'
#     )
#
#     def __str__(self):
#         return self.name