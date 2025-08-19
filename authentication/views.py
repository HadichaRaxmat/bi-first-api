from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class AuthViewSet(ViewSet):
    # --- Регистрация ---
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer()},
        operation_summary="Регистрация нового пользователя",
    )
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- Логин ---
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "Token"},
        operation_summary="Логин пользователя (email или телефон)",
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
