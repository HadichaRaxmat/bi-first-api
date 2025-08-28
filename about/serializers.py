from rest_framework import serializers
from .models import About, Founders

class FoundersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founders
        fields = ['id', 'image', 'full_name', 'position']


class AboutSerializer(serializers.ModelSerializer):
    founders = FoundersSerializer(many=True, read_only=True)
    class Meta:
        model = About
        fields = ['id', 'title', 'title2', 'description', 'founders']
