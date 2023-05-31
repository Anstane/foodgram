from colorfield.fields import ColorField
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


# class User(AbstractUser):
#     username = models.CharField(
#         'Логин',
#         max_length=50,
#         unique=True
#     )
#     email = models.EmailField(
#         'Почта',
#         max_length=100,
#         unique=True
#     )
#     first_name = models.CharField(
#         'Имя',
#         max_length=50
#     )
#     last_name = models.CharField(
#         'Фамилия',
#         max_length=50
#     )

#     def __str__(self):
#         return self.username


# class Subscribe(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     following = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         constraints = (
#             models.UniqueConstraint(
#                 fields=['user', 'following'],
#                 name='unique_user_following'
#             ),
#         )


class Tag(models.Model):
    """Модель экземпляра тегов."""

    name = models.CharField(max_length=256)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель экземпляра ингредиентов."""

    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Смежная модель ингредиентов и рецептов для корректного отображения."""

    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Recipe(models.Model):
    """Модель экземпляра рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag
    )
    ingredients = models.ManyToManyField(
        IngredientRecipe
    )
    image = models.ImageField(
        upload_to='recipes/images/', 
        null=False,
        blank=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    name = models.CharField(max_length=256)
    text = models.CharField(max_length=256)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        ordering = ['pub_date']
    
    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            ),
        )
