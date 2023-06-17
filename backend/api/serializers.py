from rest_framework import serializers, validators
from djoser.serializers import UserCreateSerializer, UserSerializer

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


class CreateCustomUserSerializer(UserCreateSerializer):
    """
    Сериализатор модели CustomUser для создания пользователя.
    """

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор модели CustomUser с проверкой на наличие подписок у юзера.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class RecipeShowSerializer(serializers.ModelSerializer):
    """
    Короткая модель рецепта для корректного отображения в разделе подписок.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(CustomUserSerializer):
    """
    Сериализатор модели подписок наследуемый от CustomUserSerializer.
    """

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
    
    def get_is_subscribed(self, obj):
        """Проверяем по фильтрам существование подписок."""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=user, author=obj
        ).exists()

    def get_recipes(self, obj):
        """
        Задаём queryset и context -
        возвращаем полученные данные из сериализатора рецептов.
        """

        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(
            author=obj
        )
        serializer = RecipeShowSerializer(
            recipes,
            many=True,
            context={'request': request}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        """Считаем количество рецептов от автора."""

        return Recipe.objects.filter(
            author=obj.author
        ).count()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для смежной модели IngredientRecipe,
    используется для обработки GET запросов.
    """

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


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления ингредиентов в рецепт.
    """

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField(write_only=True,)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)


class RecipeGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Recipe,
    принимает в себя поля без возможности редактирования,
    обрабатывает GET запросы.
    """

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientRecipeGetSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
    
    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, recipe_id=obj.id
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user, recipe_id=obj.id
            ).exists()
        return False


class RecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Recipe,
    занимается обработкой POST/UPDATE запросов.
    """
    
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = IngredientRecipePostSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
