from rest_framework import serializers
from .models import Children


class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = [
            "id",
            "first_name",
            "last_name",
            "father_name",
            "birth_date",
            "study_place",
            "type_of_kind",
        ]
        read_only_fields = ["id"]
