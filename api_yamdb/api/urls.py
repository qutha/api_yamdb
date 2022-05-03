from django.urls import path, include
from rest_framework import routers

# from .views import TitlesViewSet, CategoriesViewSet, GenresViewSet
from .views import UserViewSet, signup, token

app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'categories', CategoriesViewSet, basename='categories')
# router.register(r'genres', GenresViewSet, basename='genres')
# router.register(r'titles', TitlesViewSet, basename='titles')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
]