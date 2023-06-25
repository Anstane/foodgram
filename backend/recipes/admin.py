from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    Favorite,
    ShoppingCart
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'text',
        'cooking_time',
        'image'
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    search_fields = (
        'author',
        'name',
        'text'
    )


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )
    list_filter = (
        'ingredient',
        'recipe'
    )
    search_fields = (
        'ingredient',
        'recipe'
    )


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    list_filter = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
        'recipe'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    list_filter = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
        'recipe'
    )
