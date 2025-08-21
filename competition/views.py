from rest_framework.viewsets import ViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import CompetitionSerializer, ApplicationSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Competition, Application
from rest_framework.permissions import IsAuthenticated



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
        operation_description="Получить список всех заявок",
        responses={200: ApplicationSerializer(many=True)},
        tags=["applications"]
    )
    def list(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получить заявку по ID",
        responses={200: ApplicationSerializer(), 404: "Not Found"},
        tags=["applications"]
    )
    def retrieve(self, request, pk=None):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

