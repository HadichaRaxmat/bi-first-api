from rest_framework import serializers
from .models import Competition, Application
from home.models import Title
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from children.models import Children
from home.serializers import TitleSerializer


class CompetitionSerializer(serializers.ModelSerializer):
    title = TitleSerializer(read_only=True)
    is_finished = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ["id", "title", "description", "image", "deadline", "is_finished"]

        def get_is_finished(self, obj):
            return obj.deadline < timezone.now()

        def join_competition(request, pk):
            competition = Competition.objects.get(pk=pk)
            if competition.deadline < timezone.now():
                raise ValidationError("Конкурс уже завершён.")




class ApplicationSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Children.objects.none()
    )

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
