from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Модель экземпляра тегов."""

    name = models.CharField(max_length=256, unique=True)
    color = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель экземпляра ингредиентов."""

    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель экземпляра рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientRecipe'
    )
    image = models.ImageField(
        upload_to='recipes/', 
        null=False,
        blank=False
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=256)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
    
    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Смежная модель ингредиентов и рецептов для корректного отображения."""

    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'    
    )
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'ingredient_recipe'
        verbose_name_plural = 'ingredient_recipes'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='unique_recipe_ingredients'
            ),
        )

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


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
    
    def __str__(self):
        return f'{self.user} {self.recipe}'


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

    def __str__(self):
        return f'{self.user} {self.recipe}'
