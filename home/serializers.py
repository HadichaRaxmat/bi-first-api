from rest_framework import serializers
from .models import Header, Title, ContactUs, Subscribe, Location, ContactNumber


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
        fields = ["id", "title", "description"]


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
    contact_us = serializers.CharField(source="contact_us.title", read_only=True)

    class Meta:
        model = ContactNumber
        fields = ['id', 'contact_us', 'number', 'image']

