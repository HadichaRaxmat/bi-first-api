from rest_framework import serializers
from .models import Gallery
from home.serializers import TitleSerializer


class GallerySerializer(serializers.ModelSerializer):
    title = TitleSerializer(read_only=True)

    class Meta:
        model = Gallery
        fields = ['id', 'title', 'image', 'description', 'created_at', 'updated_at']
