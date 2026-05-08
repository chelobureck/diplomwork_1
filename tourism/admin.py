from django.contrib import admin
from .models import Place, Review, Photo

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'author', 'rating', 'visit_date', 'created_at')
    list_filter = ('rating', 'visit_date')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'review', 'created_at')
