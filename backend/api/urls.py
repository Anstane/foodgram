from django.urls import include, path
from rest_framework import routers

from .views import (
    CustomUserViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
