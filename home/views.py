from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from .serializers import HeaderSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Header


class HomeViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get Header",
        operation_summary="Get Header",
        responses={
            200: HeaderSerializer(),
        },
        tags=['home']
    )
    def header(self, request, *args, **kwargs):
        headers = Header.objects.all().first()
        serializer = HeaderSerializer(headers, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
