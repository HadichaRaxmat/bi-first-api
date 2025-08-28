from rest_framework import serializers
from .models import Result
from children.models import Children

class ResultSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = ["id", "title", "image", "description", "participants"]

    def get_participants(self, obj):
        # Берём всех уникальных детей, у которых есть заявки
        return Children.objects.filter(applications__isnull=False).distinct().count()
