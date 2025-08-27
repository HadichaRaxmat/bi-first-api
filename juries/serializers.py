from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import AddJuries
from django.contrib.auth.hashers import make_password
from competition.models import Competition

class JuryLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")

        try:
            jury = AddJuries.objects.get(login=login)
        except AddJuries.DoesNotExist:
            raise serializers.ValidationError("Неверный логин или пароль")

        # Проверка пароля (если хэширован через make_password)
        if not check_password(password, jury.password):
            raise serializers.ValidationError("Неверный логин или пароль")

        # прикрепляем найденного жюри к validated_data
        data["jury"] = jury
        return data



class JuryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddJuries
        fields = [
            "id", 'image', "first_name", "last_name", "birth_date",
            "email", "phone_number"
        ]


class JuriCompetitionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    competition = serializers.CharField()


class JuryCompetitionDetailSerializer(serializers.ModelSerializer):
    competition_title = serializers.CharField(source="title", read_only=True)

    class Meta:
        model = Competition
        fields = ["id", "title", "end_date", "participants"]


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