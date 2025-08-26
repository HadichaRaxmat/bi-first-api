from django.db import transaction
import uuid
from rest_framework import serializers
from .models import Payment
from competition.models import Application


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ["payment_id", "price", "date_time", "payment_method"]
        read_only_fields = ["date_time", "payment_id", "payment_method"]

    #  Возвращаем метод оплаты из Application
    def get_payment_method(self, obj):
        return obj.application.payment_method

    def create(self, validated_data):
        request = self.context.get("request")
        application_id = request.data.get("application_id")

        if not application_id:
            raise serializers.ValidationError({"application_id": "Это поле обязательно."})

        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            raise serializers.ValidationError({"application_id": "Заявка не найдена."})

        with transaction.atomic():
            validated_data["payment_id"] = uuid.uuid4().hex
            validated_data["application"] = application
            payment = Payment.objects.create(**validated_data)

        return payment