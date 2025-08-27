from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from competition.models import Competition
from children.models import Children
from .authentication import JuryJWTAuthentication
from .serializers import (
    JuryLoginSerializer,
    JuryProfileSerializer,
    JuryCompetitionDetailSerializer,
    JurySecuritySerializer,
    JuryCompetitionsSerializer,
    CompetitionParticipantSerializer,
    JuryGradeSerializer
    )


class JuryViewSet(ViewSet):

    # --- Логин ---
    authentication_classes = [JuryJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="login", authentication_classes=[], permission_classes=[])
    def login(self, request):
        serializer = JuryLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jury = serializer.validated_data["jury"]

        refresh = RefreshToken()
        refresh["jury_id"] = jury.id

        return Response({
            "message": "Login successful",
            "jury_id": jury.id,
            "full_name": str(jury),
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)

    # --- Профиль ---
    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="profile",
        permission_classes=[permissions.IsAuthenticated]
    )
    def profile(self, request):
        jury = request.user

        if request.method == "GET":
            serializer = JuryProfileSerializer(jury)
            return Response(serializer.data)

        if request.method == "PATCH":
            serializer = JuryProfileSerializer(jury, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- Competitions ---
    @action(detail=False, methods=["get"], url_path="competitions",
            permission_classes=[permissions.IsAuthenticated])
    def competitions(self, request):
        competitions = Competition.objects.filter(is_active=True)
        serializer = JuryCompetitionsSerializer(competitions, many=True)
        return Response(serializer.data)

    # --- Competition detail ---
    @action(detail=True, methods=["get"], url_path="competition",
            permission_classes=[permissions.IsAuthenticated])
    def competition_detail(self, request, pk=None):
        try:
            competition = Competition.objects.get(pk=pk, is_active=True)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JuryCompetitionDetailSerializer(competition)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="participants",
            permission_classes=[permissions.IsAuthenticated])
    def competition_participants(self, request, pk=None):
        try:
            competition = Competition.objects.get(pk=pk, is_active=True)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)

        applications = competition.applications.all()
        children = Children.objects.filter(applications__in=applications).distinct()
        serializer = CompetitionParticipantSerializer(children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"], url_path="participant",
            permission_classes=[permissions.IsAuthenticated])
    def participant_detail(self, request, pk=None, competition_pk=None):
        """
        GET: возвращает информацию об участнике
        POST: добавляет оценку жюри для участника
        """
        try:
            participant = Children.objects.get(pk=pk)
        except Children.DoesNotExist:
            return Response({"error": "Participant not found"}, status=status.HTTP_404_NOT_FOUND)

        # --- POST: создание оценки ---
        if request.method == "POST":
            if not competition_pk:
                return Response({"error": "Competition ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                competition = Competition.objects.get(pk=competition_pk, is_active=True)
            except Competition.DoesNotExist:
                return Response({"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()
            data["child"] = participant.id
            data["jury"] = request.user.id
            data["competition"] = competition.id

            serializer = JuryGradeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # --- GET: возвращаем данные участника ---
        serializer = CompetitionParticipantSerializer(participant)
        return Response(serializer.data)



    # --- Security (смена пароля) ---
    @action(detail=False, methods=["post"], url_path="security",
            permission_classes=[permissions.IsAuthenticated])
    def security(self, request):
        serializer = JurySecuritySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully"})

    # --- Logout ---
    @action(detail=False, methods=["post"], url_path="logout",
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    # --- Danger Zone (удаление аккаунта) ---
    @action(detail=False, methods=["delete"], url_path="danger-zone",
            permission_classes=[permissions.IsAuthenticated])
    def danger_zone(self, request):
        jury = request.user
        jury.delete()
        return Response({"message": "Account deleted"}, status=status.HTTP_204_NO_CONTENT)
