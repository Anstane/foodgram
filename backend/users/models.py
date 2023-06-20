from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Класс экземпляра пользователя."""

    email = models.EmailField(
        verbose_name='Почта',
        max_length=255,
        unique=True
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=100,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=50
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_username'
            ),
        )

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """
    Модель подписки с проверкой на уникальность
    и ограничением подписки на самого юзера.
    """

    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_follow'
            ),
        )

    def __str__(self):
        return f'{self.user} {self.author}'
