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


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit',)


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True,)
    ingredients = IngredientRecipeGetSerializer(read_only=True, many=True,)

    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True,)
    amount = serializers.IntegerField(write_only=True,)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)


class RecipePostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = IngredientRecipePostSerializer(many=True)

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
