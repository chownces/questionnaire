from rest_framework import serializers
from api.models import Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "choice", "choice_id")
