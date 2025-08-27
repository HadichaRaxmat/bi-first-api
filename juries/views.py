from .models import AddJuries
from .serializers import JuryLoginSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions



class JuryViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]


    # def retrieve(self, request, pk=None):
    #     try:
    #         jury = AddJuries.objects.get(pk=pk)
    #     except AddJuries.DoesNotExist:
    #         return Response({"error": "Jury not found"}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = JurySerializer(jury)
    #     return Response(serializer.data)
    #
    #
    # def partial_update(self, request, pk=None):
    #     try:
    #         jury = AddJuries.objects.get(pk=pk)
    #     except AddJuries.DoesNotExist:
    #         return Response({"error": "Jury not found"}, status=status.HTTP_404_NOT_FOUND)
    #
    #     serializer = JurySerializer(jury, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         password = request.data.get("password")
    #         if password:
    #             serializer.save(password=make_password(password))
    #         else:
    #             serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = JuryLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jury = serializer.validated_data["jury"]

        return Response({
            "message": "Login successful",
            "jury_id": jury.id,
            "full_name": str(jury),
        }, status=status.HTTP_200_OK)

