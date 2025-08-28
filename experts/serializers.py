from rest_framework import serializers
from .models import Expert, ExpertsSocialLink

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertsSocialLink
        fields = ['id', 'platform', 'url', 'icon']

class ExpertSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Expert
        fields = ['id', 'title', 'image', 'full_name', 'specialization', 'description', 'social_links']
