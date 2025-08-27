from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import AddJury
from django.contrib.auth.hashers import make_password
from competition.models import Competition
from juries.models import JuryGrade
from children.models import Children

class JuryLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")

        try:
            jury = AddJury.objects.get(login=login)
        except AddJury.DoesNotExist:
            raise serializers.ValidationError("Неверный логин или пароль")

        # Проверка пароля (если хэширован через make_password)
        if not check_password(password, jury.password):
            raise serializers.ValidationError("Неверный логин или пароль")

        # прикрепляем найденного жюри к validated_data
        data["jury"] = jury
        return data



class JuryProfileSerializer(serializers.ModelSerializer):
    """Профиль жюри (с возможностью частичного обновления)"""
    class Meta:
        model = AddJury
        fields = ["id", "image", "first_name", "last_name", "birth_date",
                  "email", "phone_number"]
        extra_kwargs = {
            "email": {"required": False},
            "phone_number": {"required": False},
        }


class JuryCompetitionsSerializer(serializers.ModelSerializer):
    """Список активных конкурсов (только id + название)"""
    class Meta:
        model = Competition
        fields = ["id", "title"]



class JuryCompetitionDetailSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ["id", "title", "end_date", "participants"]

    def get_participants(self, obj):
        # Берём всех детей, которые подали заявку на этот конкурс
        children = Children.objects.filter(applications__competition=obj).distinct()
        return CompetitionParticipantSerializer(children, many=True).data



class CompetitionParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = ["id", "first_name", "image"]


class JurySecuritySerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        jury = self.context['request'].jury

        # Проверка текущего пароля
        if not check_password(data['current_password'], jury.password):
            raise serializers.ValidationError({"current_password": "Неверный текущий пароль."})

        # Проверка совпадения нового пароля и подтверждения
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Пароли не совпадают."})

        # Проверка, что новый пароль не совпадает со старым
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError({"new_password": "Новый пароль не может совпадать с текущим."})

        return data

    def save(self, **kwargs):
        jury = self.context['request'].jury
        jury.password = make_password(self.validated_data['new_password'])
        jury.save()
        return jury


class JuryGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuryGrade
        fields = ["id", "score", "comment"]

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Оценка должна быть от 1 до 10.")
        return value


