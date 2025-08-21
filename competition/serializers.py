from rest_framework import serializers
from .models import Competition, Application
from home.models import Title
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from children.models import Children
from home.serializers import TitleSerializer



class CompetitionSerializer(serializers.ModelSerializer):
    title = TitleSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ["id", "title", "description", "image", "start_date", "end_date", "age", "status"]

    def get_status(self, obj):
        today = timezone.now().date()
        return "finished" if obj.end_date < today else "active"



class ApplicationSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Children.objects.none())

    class Meta:
        model = Application
        fields = ['id', 'competition', 'children', 'physical_certificate', 'payment_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and hasattr(request, "user"):
            user = request.user
            self.fields['children'].queryset = Children.objects.filter(parent=user)

    def create(self, validated_data):
        children = validated_data.pop('children', [])
        request = self.context.get('request')
        parent = request.user if request else None

        application = Application.objects.create(
            parent=parent,
            **validated_data
        )
        application.children.set(children)
        return application
