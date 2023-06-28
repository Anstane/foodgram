from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

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
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """Сериализатор модели CustomUser."""

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
        """Проверяем есть ли у пользователя подписки."""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class RecipeShowSerializer(serializers.ModelSerializer):
    """
    Короткая модель рецепта для корректного отображения в разделе подписок.
    """

    image = Base64ImageField()

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
        """Проверяем существование подписок."""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(
            user=user, author=obj
        ).exists()

    def get_recipes(self, obj):
        """
        Фильтруем рецепты + получаем context и передаём
        это в сериализатор рецепта созданный для подписок.
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
            author=obj
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


class RecipeGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки GET запросов модели Recipe.
    """

    author = CustomUserSerializer()
    tags = TagSerializer(
        many=True
    )
    ingredients = IngredientRecipeGetSerializer(
        many=True, source='ingredient_recipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Ищем объект в модели Favorite."""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Ищем объект в модели ShoppingCart."""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user, recipe=obj
        ).exists()


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор колчества ингредиента в рецепте.
    """

    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Recipe - POST и PATCH методы.
    """

    author = serializers.HiddenField(
        default=CustomUserSerializer()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    ingredients = IngredientRecipePostSerializer(
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate_tags(self, value):
        """Валидируем наличие тега."""

        if not value:
            raise serializers.ValidationError(
                "Нужно передать как минимум 1 тег."
            )
        return value

    def validate_ingredients(self, value):
        """Валидируем наличие и уникальность ингредиентов."""

        if not value:
            raise serializers.ValidationError(
                "Нужно передать как минимум 1 ингредиент."
            )

        ingredient_list = []
        for ingredient in value:
            if ingredient['id'] in ingredient_list:
                raise serializers.ValidationError(
                    "Добавить можно только уникальные ингедиенты."
                )
            ingredient_list.append(ingredient['id'])
        return value

    def add_ingredients(self, ingredients, recipe):
        """Метод для добавления ингредиентов в рецепт."""

        ingredient_list = [
            IngredientRecipe(
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
            for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        """
        Метод create, в котором мы передаём теги и ингредиенты.
        """

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """
        Очищаем старые поля от исходных данных и
        с помощью метода super() записываем новые данные.
        """

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.set(tags)
        instance.ingredient_recipe.all().delete()
        self.add_ingredients(ingredients, instance)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Переопределяем метод to_representation
        для корретного отбражения JSON`а
        после POST или PATCH запроса.
        """

        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(instance, context=context).data
