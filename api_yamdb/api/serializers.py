from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Categories, Genres, Titles, Review


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