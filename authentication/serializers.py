from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import User
from django.contrib.auth import authenticate
from .models import EmailVerification
from .utils import send_verification_email
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password


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

        code = EmailVerification.generate_code()
        EmailVerification.objects.create(user=user, code=code)
        send_verification_email(user)

        return user


class EmailVerificationSerializer(serializers.Serializer):
    code = serializers.SlugField(max_length=32)

    def validate(self, data):
        code = data['code']

        verification = EmailVerification.objects.filter(code=code).first()
        if not verification:
            raise serializers.ValidationError('Code not found')

        user = verification.user
        if not user:
            raise serializers.ValidationError('Code is invalid')

        if not user.email:
            raise serializers.ValidationError('Unknown error')

        if verification.is_expired():
            raise serializers.ValidationError('Code is expired')

        verification.delete()

        data['user'] = user
        return data



class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        if getattr(user, "email_verified", False):  # если уже подтвержден
            raise serializers.ValidationError({"email": "This email is already verified."})

        data["user"] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data["user"]

        # Удаляем старые коды
        EmailVerification.objects.filter(user=user).delete()

        # Создаём новый код
        code = EmailVerification.generate_code()
        EmailVerification.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # Отправляем письмо заново
        send_verification_email(user)

        return code




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




class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["image", "email", "phone", "first_name", "last_name", "birth_date"]
        read_only_fields = ['birth_date']



class SecuritySerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # Проверка текущего пароля
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({"current_password": "Неверный текущий пароль."})

        # Проверка совпадения нового пароля и подтверждения
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Пароли не совпадают."})

        # Проверка, что новый пароль не совпадает со старым
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError({"new_password": "Новый пароль не может совпадать с текущим."})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user




class DangerZoneSerializer(serializers.Serializer):
    def save(self, **kwargs):
        user = self.context['request'].user
        user.delete()
        return {"detail": "Аккаунт успешно удалён."}



from competition.models import Application, Competition
from django.utils import timezone

class MyCompetitionSerializer(serializers.ModelSerializer):
    competition = serializers.CharField(source="competition.title", read_only=True)

    class Meta:
        model = Application
        fields = ["id", "competition"]


class MySubscribedCompetitionSerializer(serializers.ModelSerializer):
    competition = serializers.CharField(source="title", read_only=True)

    class Meta:
        model = Competition
        fields = ["id", "competition"]


class CompetitionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    competition = serializers.CharField()


class CompetitionDetailSerializer(serializers.ModelSerializer):
    competition_title = serializers.CharField(source="title", read_only=True)

    class Meta:
        model = Competition
        fields = ["id", "title", "about_competition", "end_date", "participants"]



