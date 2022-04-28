from django.urls import include, path
from rest_framework import routers

from .views import TitlesViewSet, CategoriesViewSet, GenresViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
