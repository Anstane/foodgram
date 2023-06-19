from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, decorators, status
from rest_framework.response import Response
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
    RecipePostSerializer,
    RecipeShowSerializer
)

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_sub(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @decorators.action(
        detail=False,
        methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def post_del_sub(self, request):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if request.method == 'POST':
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            subsctiption = get_object_or_404(
                Subscribe, user=user, author=author
            )
            subsctiption.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    # filter_backends = 


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAdminOrReadOnly,)
    # filter_backends = 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeShowSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if self.request.method == 'DELETE':
            favorite = Favorite.objects.get(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if self.request.method == 'POST':
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShowSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if self.request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.get(user=user, recipe=recipe)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @decorators.action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        pass