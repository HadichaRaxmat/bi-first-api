from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from .serializers import CompetitionSerializer, ApplicationSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Competition, Application


class CompetitionViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all competitions",
        operation_summary="Get all competitions",
        responses={200: CompetitionSerializer()},
        tags=['competition']
    )
    def get(self, request, *args, **kwargs):
        competitions = Competition.objects.all()
        if not competitions:
            return Response({"detail": "No competitions found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompetitionSerializer(competitions, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class ApplicationViewSet(ViewSet):

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

