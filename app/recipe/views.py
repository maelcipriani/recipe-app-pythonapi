"""
Views for the recipe app.
"""
from collections import defaultdict

import django_filters
from django.db.models import Count
from rest_framework import viewsets, mixins, filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from core.models import Recipe, Tag
from . import serializers


class RecipePriceFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Recipe
        fields = ['price']


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Recipe model."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""

        userId = self.request.query_params.get('userId')

        if userId:
            queryset = Recipe.objects.filter(user__id=userId)

            return queryset

        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user).order_by('-id')
        return self.queryset

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)




class TagViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for the Tag model."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Retrieve the tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag."""
        serializer.save(user=self.request.user)




