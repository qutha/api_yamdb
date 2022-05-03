from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from reviews.models import Categories, Genres, Titles
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('rating'))['rating__avg']


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')




class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Genres.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')



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
        read_only_fields = ('role',)


class RegisterUserSerializer(serializers.ModelSerializer, ValidateUsername):

    class Meta:
        model = User
        fields = ('email', 'username', )


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')