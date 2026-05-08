from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Review, Photo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'place', 'review', 'created_at')

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author_avatar = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'place', 'author', 'author_name', 'author_avatar', 'rating', 'text', 'visit_date', 'likes_count', 'photos', 'created_at')
        read_only_fields = ('author', 'likes_count')

    def get_author_avatar(self, obj):
        # Assuming we might add an avatar later or just use a placeholder
        return None

class PlaceSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Place
        fields = ('id', 'name', 'description', 'category', 'latitude', 'longitude', 'average_rating', 'review_count', 'photos', 'created_by', 'created_at')
        read_only_fields = ('created_by',)
