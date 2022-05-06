from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """
    Добавление к стандартной модели User полей с биографией и ролью.
    """
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=CHOICES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username} - {self.email}'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
