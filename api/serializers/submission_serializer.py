from rest_framework import serializers
from api.models import Answer, Question, Submission
from . import AnswerSerializer, FormSerializer, QuestionSerializer


class SubmissionWriteSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    INVALID_ANSWERS_LENGTH_MESSAGE = (
        "Number of answers do not match the number of questions in form!"
    )
    INVALID_QUESTION_TYPE_MESSAGE = "Invalid question type in answers array!"
    INVALID_QUESTION_TYPE_MATCH_MESSAGE = (
        "Question types do not match the specified form!"
    )

    class Meta:
        model = Submission
        fields = "__all__"

    def create(self, validated_data):
        answers = validated_data.pop("answers")
        form_id = validated_data["form_id"]

        submission_instance = Submission.objects.create(form_id=form_id)
        question_instances = Question.objects.filter(form_id=form_id).order_by(
            "display_order"
        )

        for idx, answer in enumerate(answers):
            Answer.objects.create(
                question_id=question_instances[idx],
                answer=answer["answer"],
                submission_id=submission_instance,
            )

        return submission_instance

    def validate(self, data):
        form_id = data["form_id"]
        answers = data["answers"]

        question_instances = Question.objects.filter(form_id=form_id).order_by(
            "display_order"
        )

        # NOTE: Assumes that answers given in display_order of questions

        # Validate number of answers provided
        if len(question_instances) != len(answers):
            raise serializers.ValidationError(self.INVALID_ANSWERS_LENGTH_MESSAGE)

        # Validate that the answer 'question types' are valid, and match the corresponding question
        question_types = list(map(lambda e: e[0], Question.QuestionTypes))
        for idx, answer in enumerate(answers):
            if answer["question_type"] not in question_types:
                raise serializers.ValidationError(self.INVALID_QUESTION_TYPE_MESSAGE)
            if answer["question_type"] != question_instances[idx].question_type:
                raise serializers.ValidationError(
                    self.INVALID_QUESTION_TYPE_MATCH_MESSAGE
                )

        # TODO: Future extension. Validate the answer format based on the question type.

        return data


class SubmissionReadSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    form_id = FormSerializer()

    class Meta:
        model = Submission
        fields = "__all__"
