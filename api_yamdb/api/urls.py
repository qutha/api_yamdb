from django.urls import path, include
from rest_framework import routers

from .views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet, UserViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]