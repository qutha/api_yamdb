from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

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


class TitleReadSerializer(ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'description', 'year', 'genre', 'category', 'rating',)
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        return rating


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class ValidateUsername:

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя \'me\' запрещено!'
            )
        return username


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all(),
                            message="Username должен быть уникальным"),
        ),
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all(),
                            message="Emain должен быть уникальным"),
        ),
    )

    class Meta:
        model = User
        fields = ('username',
                  'email', 'first_name', 'last_name', 'bio', 'role')


class UserRoleOnlyReadSerializer(UserSerializer):
    role = serializers.StringRelatedField(read_only=True)


class RegisterUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', )


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')