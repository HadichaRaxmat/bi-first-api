from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Введите корректный номер (от 10 до 15 цифр, можно с '+')."
            )
        ]
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "father_name",
            "birth_date",
        ]

    def validate(self, data):
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not email and not phone:
            raise serializers.ValidationError("Нужно указать email или номер телефона.")

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует."})

        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "Пользователь с таким номером уже существует."})

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Пароли не совпадают"})

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email_or_phone = data.get("email_or_phone")
        password = data.get("password")

        if not email_or_phone or not password:
            raise serializers.ValidationError("Введите email/телефон и пароль.")

        # Проверяем, по чему логинимся
        try:
            if "@" in email_or_phone:  # email
                user = User.objects.get(email=email_or_phone)
            else:  # телефон
                user = User.objects.get(phone=email_or_phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный email или номер телефона.")

        # Проверяем пароль
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Неверный пароль.")

        data["user"] = user
        return data
