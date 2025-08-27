from rest_framework.authtoken.models import Token
from .serializers import (RegisterSerializer, LoginSerializer, EmailVerificationSerializer, ResendEmailVerificationSerializer,
                          PersonalInfoSerializer, SecuritySerializer, DangerZoneSerializer)
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
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




from competition.models import Application, Competition
from .serializers import (MyCompetitionSerializer, MySubscribedCompetitionSerializer, CompetitionResponseSerializer,
                          CompetitionDetailSerializer)
from django.utils import timezone
from django.db.models import Q
from drf_yasg import openapi


class AccountViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="get profile",
        operation_id="get profile",
        responses={200: PersonalInfoSerializer()},
        tags=["Account"],
    )
    # ---------- Персональная информация ----------
    def retrieve(self, request, pk=None):
        """
        GET /account/ — получить данные пользователя
        """
        serializer = PersonalInfoSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update profile",
        operation_id="Update profile",
        responses={200: PersonalInfoSerializer()},
        tags=["Account"],
    )
    def partial_update(self, request, pk=None):
        """
        PATCH /account/ — обновить данные пользователя
        """
        serializer = PersonalInfoSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    # ---------- Мои конкурсы ----------
    status_param = openapi.Parameter(
        'status',
        openapi.IN_QUERY,
        description="Фильтр по статусу (subscriptions | active | finished)",
        type=openapi.TYPE_STRING,
        enum=['subscriptions', 'active', 'finished']
    )

    @swagger_auto_schema(
        operation_description="Получить список моих конкурсов по статусу",
        operation_id="Get my competitions",
        manual_parameters=[status_param],
        responses={
            200: openapi.Response(
                description="Список моих конкурсов",
                schema=CompetitionResponseSerializer(many=True),
                examples={
                    "application/json": [
                        {"id": 1, "competition": "Мой первый конкурс"},
                        {"id": 2, "competition": "Летний марафон"}
                    ]
                }
            ),
            400: openapi.Response(description="Неверный статус")
        },
        tags=["Account"]
    )
    @action(detail=False, methods=['get'], url_path='my-competitions')
    def my_competitions(self, request):
        status_filter = request.query_params.get("status")
        today = timezone.now().date()

        if status_filter == "subscriptions":
            competitions = Competition.objects.filter(subscribers__subscriber=request.user)
            serializer = MySubscribedCompetitionSerializer(competitions, many=True)

        elif status_filter == "active":
            applications = Application.objects.filter(
                parent=request.user
            ).filter(
                Q(competition__end_date__gte=today) | Q(competition__end_date__isnull=True)
            )
            serializer = MyCompetitionSerializer(applications, many=True)

        elif status_filter == "finished":
            applications = Application.objects.filter(
                parent=request.user,
                competition__end_date__lt=today
            )
            serializer = MyCompetitionSerializer(applications, many=True)

        else:
            return Response({"detail": "Неверный статус"}, status=400)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Competition detail",
        operation_id="Competition detail",
        responses={200: CompetitionDetailSerializer()},
        tags=["Account"],
    )
    @action(detail=True, methods=["get"], url_path="competition")
    def competition_detail(self, request, pk=None):
        """
        Получить детальную информацию о конкурсе, на который подана заявка.
        pk — это ID Application.
        """
        try:
            application = Application.objects.get(id=pk, parent=request.user)
        except Application.DoesNotExist:
            return Response({"detail": "Заявка не найдена или доступ запрещён"}, status=status.HTTP_404_NOT_FOUND)

        competition = application.competition
        serializer = CompetitionDetailSerializer(competition)
        return Response(serializer.data)


    # ---------- Смена пароля ----------
    @swagger_auto_schema(
        operation_description="Change password",
        operation_id="Change password",
        responses={200: SecuritySerializer()},
        tags=["Account"],
    )
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = SecuritySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно изменён."}, status=status.HTTP_200_OK)

    # ---------- Удаление аккаунта ----------
    @swagger_auto_schema(
        operation_description="Delete account",
        operation_id="Delete account",
        responses={200: DangerZoneSerializer()},
        tags=["Account"],
    )
    @action(detail=False, methods=['post'], url_path='delete-account')
    def delete_account(self, request):
        serializer = DangerZoneSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)



