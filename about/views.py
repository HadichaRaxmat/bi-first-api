from rest_framework import viewsets
from rest_framework.response import Response
from .models import About
from .serializers import AboutSerializer
from drf_yasg.utils import swagger_auto_schema

class AboutViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Get About section with founders",
        operation_summary="Get About section with founders",
        responses={200: AboutSerializer(many=True)},
        tags=['about']
    )
    def list(self, request):
        queryset = About.objects.prefetch_related('founders').all()
        serializer = AboutSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
