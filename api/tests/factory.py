from factory import django, Faker, SubFactory

from api.models import Answer, Choice, Form, Question, Submission


class FormFactory(django.DjangoModelFactory):
    class Meta:
        model = Form

    title = Faker("sentence")


QUESTION_TYPE_VALUES = [x[0] for x in Question.QuestionTypes]


class QuestionFactory(django.DjangoModelFactory):
    class Meta:
        model = Question

    question_type = Faker("random_element", elements=QUESTION_TYPE_VALUES)
    question = Faker("sentence")
    display_order = 1
    form_id = SubFactory(FormFactory)


class SubmissionFactory(django.DjangoModelFactory):
    class Meta:
        model = Submission

    form_id = SubFactory(FormFactory)


class AnswerFactory(django.DjangoModelFactory):
    class Meta:
        model = Answer

    # TODO: Future extension. To be updated when there is input validation for different question types
    answer = Faker("sentence")
    question_id = SubFactory(QuestionFactory)
    submission_id = SubFactory(SubmissionFactory)


class ChoiceFactory(django.DjangoModelFactory):
    class Meta:
        model = Choice

    question_id = SubFactory(QuestionFactory)
    choice_id = 1
    choice = Faker("sentence")
