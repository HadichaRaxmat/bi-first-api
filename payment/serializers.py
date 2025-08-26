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

    def get_payment_method(self, obj):
        return obj.application.payment_method

    def validate(self, attrs):
        request = self.context.get("request")
        application_id = request.data.get("application_id")

        if not application_id:
            raise serializers.ValidationError({"application_id": "Это поле обязательно."})

        try:
            application = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            raise serializers.ValidationError({"application_id": "Заявка не найдена."})

        if not application.payment_method:
            raise serializers.ValidationError({"payment_method": "Метод оплаты не выбран в заявке."})

        if application.payments.exists():
            raise serializers.ValidationError({"application": "Для этой заявки уже есть платеж."})

        attrs["application"] = application
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["payment_id"] = uuid.uuid4().hex
            payment = Payment.objects.create(**validated_data)
        return payment
