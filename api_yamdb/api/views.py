from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Genres, Titles
from .serializers import (
    CategoriesSerializer, GenresSerializer, TitlesSerializer
)
from .permissions import IsAdminOrReadOnly


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
