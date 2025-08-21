from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer, ResendEmailVerificationSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class AuthViewSet(ViewSet):
    # --- Регистрация ---
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: RegisterSerializer()},
        operation_summary="Регистрация нового пользователя",
        tags=["Authentication"],
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
        tags=["Authentication"],
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Email verification",
        operation_id="Email verification",
        responses={200: EmailVerificationSerializer()},
        tags=["Authentication"],
    )

    def post(self, request):
        verify_serializer = EmailVerificationSerializer(data=request.data)
        if verify_serializer.is_valid():
            user = verify_serializer.validated_data['user']
            user.email_verified = True
            user.save()
            return Response({'message': 'Account is successfully confirmed'}, status=status.HTTP_200_OK)
        return Response(verify_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Resend verification email",
        operation_id="Resend verification email",
        responses={200: EmailVerificationSerializer()},
        tags=["Authentication"],
    )

    @action(detail=False, methods=["post"])
    def resend(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Verification email resent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)