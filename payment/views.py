from rest_framework.viewsets import ViewSet
from serializers import PaymentSerializer
from rest_framework import status
from rest_framework.response import Response



class CompetitionPaymentViewSet(ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)