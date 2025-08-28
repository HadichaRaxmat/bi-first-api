from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import ResultSerializer
from .models import Result

class ResultViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Получить все результаты",
        operation_summary="Список результатов",
        responses={200: ResultSerializer(many=True)},
        tags=['results']
    )
    def list(self, request):
        results = Result.objects.all()
        if not results.exists():
            return Response({"detail": "Нет результатов"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)