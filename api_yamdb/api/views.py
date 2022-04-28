from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api_yamdb.api.serializers import ReviewSerializer
from api_yamdb.reviews.models import Review


class ReviewView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer