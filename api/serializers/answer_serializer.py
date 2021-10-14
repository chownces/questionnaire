from rest_framework import serializers
from api.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    question_type = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Answer
        fields = ("id", "answer", "question_id", "question_type")
        read_only_fields = ("question_id",)
