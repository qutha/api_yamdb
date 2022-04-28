from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    bio = models.TextField(verbose_name='Биография',
                           blank=True,)
    role = models.CharField(verbose_name='Роль',
                            max_length=50,
                            choices=CHOICES,
                            default='user')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} - {self.email}'