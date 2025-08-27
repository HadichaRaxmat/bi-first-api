from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AddJury


class JuryJWTAuthentication(JWTAuthentication):
    """
    Аутентификация жюри через JWT (без User).
    """

    def get_user(self, validated_token):
        try:
            jury_id = validated_token["jury_id"]
        except KeyError:
            raise AuthenticationFailed("Токен недействителен: нет jury_id")

        try:
            return AddJury.objects.get(id=jury_id)
        except AddJury.DoesNotExist:
            raise AuthenticationFailed("Жюри не найдено")