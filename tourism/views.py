from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from .models import Place, Review, Photo
from .serializers import PlaceSerializer, ReviewSerializer, PhotoSerializer, UserSerializer

class UserRegistrationView(generics.CreateAPIView):
    # Avoid evaluating a queryset at import time (can trigger DB access during migrations)
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def top(self, request):
        # Top places by average rating
        top_places = Place.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            count_reviews=Count('reviews')
        ).filter(count_reviews__gt=0).order_by('-avg_rating')[:10]
        serializer = self.get_serializer(top_places, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.all()
        place_id = self.request.query_params.get('place_id')
        if place_id:
            queryset = queryset.filter(place_id=place_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        review = self.get_object()
        review.likes_count += 1
        review.save()
        return Response({'status': 'liked', 'likes_count': review.likes_count})

    @action(detail=False, methods=['get'])
    def top(self, request):
        # Top reviews by likes
        top_reviews = Review.objects.order_by('-likes_count')[:10]
        serializer = self.get_serializer(top_reviews, many=True)
        return Response(serializer.data)

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file = request.data.get('image')
        place_id = request.data.get('place')
        review_id = request.data.get('review')
        
        photo = Photo.objects.create(image=file, place_id=place_id, review_id=review_id)
        return Response(PhotoSerializer(photo).data, status=status.HTTP_201_CREATED)
