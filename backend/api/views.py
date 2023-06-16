from rest_framework import viewsets, permissions
from djoser.views import UserViewSet

from .pagination import (
    CustomPagination
)
from .permissions import (
    IsAuthorOrReadOnly,
    IsAdminOrReadOnly
)
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
from .serializers import (
    CustomUserSerializer,
    SubscribeSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipePostSerializer
)

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer
