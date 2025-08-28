from rest_framework import viewsets
from rest_framework.response import Response
from .models import Expert
from .serializers import ExpertSerializer

class ExpertViewSet(viewsets.ViewSet):

    def list(self, request):
        experts = Expert.objects.all()
        serializer = ExpertSerializer(experts, many=True, context={'request': request})
        return Response(serializer.data)




