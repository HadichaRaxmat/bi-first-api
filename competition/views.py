from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import CompetitionSerializer, ApplicationSerializer, CompetitionSubscriberSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Competition, Application, CompetitionSubscriber
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class CompetitionViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get all competitions",
        operation_summary="Get all competitions",
        responses={200: CompetitionSerializer(many=True)},
        tags=['competition']
    )
    def list(self, request):
        competitions = Competition.objects.all().order_by('-end_date')

        if not competitions.exists():
            return Response({"detail": "No competitions found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompetitionSerializer(competitions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class ApplicationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Создать новую заявку",
        request_body=ApplicationSerializer,
        responses={201: ApplicationSerializer(), 400: "Bad Request"},
        tags=["applications"]
    )
    def create(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user)

    @swagger_auto_schema(
        operation_description="Subscribe",
        request_body=CompetitionSubscriberSerializer,
        responses={201: CompetitionSubscriberSerializer(), 400: "Bad Request"},
        tags=["applications"]
    )
    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        """
        POST /applications/subscribe/ — подписка на конкурс
        body: { "competition": <id конкурса> }
        """
        serializer = CompetitionSubscriberSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Подписка создана"}, status=status.HTTP_201_CREATED)
