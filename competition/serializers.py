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
        fields = ["id", "title", "description", "image", "age", "start_date", "end_date", "status"]

    def get_status(self, obj):
        today = timezone.now().date()
        if obj.end_date is None:
            return "no_end_date"
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

    def validate(self, attrs):
        competition = attrs.get("competition")
        children = attrs.get("children", [])

        # Парсим минимальный возраст из competition.age (например, "+12")
        try:
            min_age = int(str(competition.age).replace("+", "").strip())
        except ValueError:
            raise serializers.ValidationError("Некорректное значение age в Competition")

        today = timezone.now().date()

        # Проверяем возраст каждого ребёнка
        for child in children:
            if not child.date_of_birth:
                raise serializers.ValidationError(f"У ребёнка {child} не указана дата рождения")

            # Вычисляем возраст
            age = today.year - child.date_of_birth.year - (
                (today.month, today.day) < (child.date_of_birth.month, child.date_of_birth.day)
            )

            if age < min_age:
                raise serializers.ValidationError(
                    f"Ребёнок {child} слишком мал для участия. Минимальный возраст: {min_age}"
                )

        return attrs

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

