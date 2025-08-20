from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Gallery
from .serializers import GallerySerializer


class GalleryViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all galleries",
        operation_summary="List Galleries",
        responses={200: GallerySerializer(many=True)},
        tags=['gallery']
    )
    def list(self, request, *args, **kwargs):
        galleries = Gallery.objects.all()
        serializer = GallerySerializer(galleries, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

