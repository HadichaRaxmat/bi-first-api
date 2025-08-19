from rest_framework import serializers
from .models import Competition, Child, Application
from home.models import Title
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ["id", "name"]


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




class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ["id", "name", "birth_date"]



class ApplicationSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Child.objects.all()
    )

    class Meta:
        model = Application
        fields = ["id", "competition", "children", "physical_certificate", "payment_method"]
