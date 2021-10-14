from rest_framework import serializers
from api.models import Choice, Question
from . import ChoiceSerializer


class QuestionSerializer(serializers.ModelSerializer):
    # Not required, to account for textbox questions which do not contain choices
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "display_order", "question", "question_type", "choices")
