from rest_framework import serializers
from api.models import Choice, Form, Question
from . import QuestionSerializer


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    INVALID_DISPLAY_ORDER_MESSAGE = (
        "display_order must be in running order starting from 1!"
    )
    INVALID_CHOICE_ID_MESSAGE = "choice_id must be in running order starting from 1!"
    INVALID_QUESTION_TYPE_WITH_CHOICES_MESSAGE = (
        "The textbox question type does not support choices!"
    )
    NO_CHOICES_SPECIFIED_MESSAGE = (
        "Radio and Checkbox questions must have at least 1 choice!"
    )

    class Meta:
        model = Form
        fields = "__all__"

    def create(self, validated_data):
        questions = validated_data.pop("questions")

        form_instance = Form.objects.create(title=validated_data["title"])

        # Handle creation of questions and corresponding choices
        for question in questions:
            choices = []
            if "choices" in question:
                choices = question.pop("choices")

            question_instance = Question.objects.create(
                **question,
                form_id=form_instance,
            )

            choices = map(
                lambda c: Choice.objects.create(**c, question_id=question_instance),
                choices,
            )

            question_instance.choices.set(choices)

        return form_instance

    def update(self, instance, validated_data):
        # NOTE: For a simplified implementation, this method does a cascading delete on all existing questions,
        # choices, submissions, answers in this form. As a result, updating a form would cause existing submissions
        # and answers to be lost.
        instance.questions.all().delete()

        instance.title = validated_data["title"]
        questions = validated_data.pop("questions")

        # Handle recreation of questions and corresponding choices
        for question in questions:
            choices = []
            if "choices" in question:
                choices = question.pop("choices")

            question_instance = Question.objects.create(
                **question,
                form_id=instance,
            )

            choices = map(
                lambda c: Choice.objects.create(**c, question_id=question_instance),
                choices,
            )

            question_instance.choices.set(choices)

        instance.save()
        return instance

    def validate(self, data):

        # Input: List of objects, and the field to check for running order. One-indexed.
        def check_running_order(arr, field):
            order_id_exists = [False for i in range(len(arr))]

            for e in arr:
                order_id = e[field]
                if order_id < 1 or order_id > len(arr):
                    return False
                order_id_exists[order_id - 1] = True
            if False in order_id_exists:
                return False

            return True

        QUESTION_TYPES_WITH_CHOICES = ["RADIO", "CHECKBOX"]

        def validate_choices(question):
            choices = []
            if "choices" in question:
                choices = question["choices"]

            # If choices are given for non choice-based questions, raise an error
            if choices and question["question_type"] not in QUESTION_TYPES_WITH_CHOICES:
                raise serializers.ValidationError(
                    self.INVALID_QUESTION_TYPE_WITH_CHOICES_MESSAGE
                )

            # If no choices are given for choice-based questions, raise an error
            if not choices and question["question_type"] in QUESTION_TYPES_WITH_CHOICES:
                raise serializers.ValidationError(self.NO_CHOICES_SPECIFIED_MESSAGE)

            # If question choice_id's are not in running order, raise an error
            if not check_running_order(choices, "choice_id"):
                raise serializers.ValidationError(self.INVALID_CHOICE_ID_MESSAGE)

        questions = data["questions"]

        if not check_running_order(questions, "display_order"):
            raise serializers.ValidationError(self.INVALID_DISPLAY_ORDER_MESSAGE)

        list(map(validate_choices, questions))

        return data
