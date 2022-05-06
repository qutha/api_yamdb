from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Используется для создания и редактирования произведений.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'description', 'year', 'genre', 'category',)
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.
    Используется для методов группы SAFE_METHODS.
    """
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'description', 'year', 'genre', 'category',
                  'rating',)
        model = Title

    def get_rating(self, obj):
        """
        Метод возвращает рейтинг произведения на основании средней оценки
        выставляемой ревьюерами для данного произвденения.
        """
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if not rating:
            return rating
        return round(rating, 1)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        """
        Метод проверяет существует ли ревью на данное произведение от данного
        ревьюера. Возвращает провалидированные данные, если ревьюер дал первый
        отзыв. Иначе возвращает исключение.
        """
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(author=author, title=title_id).exists():
                raise serializers.ValidationError(
                    'У автора может быть лишь один отызв на одно произведение!'
                )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    username = serializers.CharField(
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username должен быть уникальным"
                ),
        ),
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message="Emain должен быть уникальным"
                ),
        ),
    )

    class Meta:
        model = User
        fields = ('username',
                  'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, username):
        """Метод проверяет, что имя пользователя не равно "ме"."""
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя \'me\' запрещено!'
            )
        return username


class UserRoleOnlyReadSerializer(UserSerializer):
    """Сериализатор для модели User без возможности редакторивания роли."""
    role = serializers.StringRelatedField(read_only=True)


class RegisterUserSerializer(UserSerializer):
    """Сериализатор для модели User для регистрации нового пользователя."""
    class Meta:
        model = User
        fields = ('email', 'username',)


class AccessTokenSerializer(serializers.Serializer):
    """Сериализатор для модели User для получения токена аутентификации."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
