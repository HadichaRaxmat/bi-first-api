from rest_framework import viewsets
from rest_framework.response import Response
from .models import Expert
from .serializers import ExpertSerializer
from drf_yasg.utils import swagger_auto_schema

class ExpertViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="get experts",
        operation_summary="get experts",
        responses={200: ExpertSerializer(many=True)},
        tags=['experts']
    )
    def list(self, request):
        experts = Expert.objects.all()
        serializer = ExpertSerializer(experts, many=True, context={'request': request})
        return Response(serializer.data)




