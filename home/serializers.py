from rest_framework import serializers
from .models import Header, Title


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'name']



class Title2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ['id', 'name', 'name2']


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ['id', 'title', 'description', 'bg_image']

