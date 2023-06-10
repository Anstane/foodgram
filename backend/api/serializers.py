from rest_framework import serializers, validators

from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    Favorite,
    ShoppingCart
)
from users.models import (
    CustomUser,
    Subscribe
)


# UserSerializer - djoser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


# Здесь нужно сделать все поля - ReadOnly
class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = '__all__'


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,)
    ingredients = IngredientRecipeSerializer(read_only=True, many=True,)

    class Meta:
        model = Recipe
        fields = '__all__'

# Отдельный класс для публикации рецептов
# Здесь нужно сделать так, чтобы поля ingredients и tags можно было записывать
class RecipePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'


# Пока не трогаем
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


# Пока не трогаем
class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
