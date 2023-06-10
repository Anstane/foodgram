from django.urls import include, path

from rest_framework import routers

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipe', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls))
]