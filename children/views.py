from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import AddChildren
from .serializers import AddChildrenSerializer


class AddChildrenViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Список детей текущего пользователя",
        responses={200: AddChildrenSerializer(many=True)},
        tags=["children"]
    )
    def list(self, request):
        children = AddChildren.objects.filter(parent=request.user)
        serializer = AddChildrenSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Добавить ребёнка",
        request_body=AddChildrenSerializer,
        responses={201: AddChildrenSerializer()},
        tags=["children"]
    )
    def create(self, request):
        serializer = AddChildrenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Удалить ребёнка",
        tags=["children"]
    )
    def destroy(self, request, pk=None):
        try:
            child = AddChildren.objects.get(pk=pk, parent=request.user)
        except AddChildren.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        child.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
