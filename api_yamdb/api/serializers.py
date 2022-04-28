from rest_framework.serializers import ModelSerializer

from api_yamdb.reviews.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')