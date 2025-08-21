from rest_framework import serializers
from .models import Header, Title, ContactUs, Subscribe, Location, ContactNumber, SocialMedia, Result


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



class ContactUsSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField()

    class Meta:
        model = ContactUs
        fields = ["id", "title", 'name', "description"]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ["id", "email"]


class LocationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="title.title", read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'title', 'image']


class ContactNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactNumber
        fields = ['id', 'number', 'image']
        read_only_fields = ['id']


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'title', 'image', 'url']


class ResultSerializer(serializers.ModelSerializer):
    title = TitleSerializer(read_only=True)

    class Meta:
        model = Result
        fields = ["id", "title", "image", "number", "description"]