
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

# from reviews.models import Categories, Genres, Titles, Reviews
from .permissions import IsAdminOrReadOnly

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import viewsets, status
from rest_framework.response import Response

from users.models import User
from .serializers import UserSerializer, RegisterUserSerializer, AccessTokenSerializer, UserRoleOnlyReadSerializer
from .services import send_confirmation_code
from .permissions import IsAdminRole, IsModeratorRole


# class ReviewView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#
# class TitlesViewSet(viewsets.ModelViewSet):
#     queryset = Titles.objects.all()
#     serializer_class = TitlesSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
#
#
# class CategoriesViewSet(viewsets.ModelViewSet):
#     queryset = Categories.objects.all()
#     serializer_class = CategoriesSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)
#
#
# class GenresViewSet(viewsets.ModelViewSet):
#     queryset = Genres.objects.all()
#     serializer_class = GenresSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = PageNumberPagination
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = (IsAdminRole, )
    search_fields = ('username',)

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'], permission_classes=(IsAuthenticated,))
    def current_user(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserRoleOnlyReadSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = AccessTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    access_token = RefreshToken.for_user(user)
    return Response(
        {'token': str(access_token.access_token)}, status=status.HTTP_200_OK
    )
