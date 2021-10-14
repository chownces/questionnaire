from api.models import Form, Question
from api.serializers import FormSerializer, QuestionSerializer
from api.views import FormViewSet
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .factory import FormFactory, QuestionFactory


class FormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Corresponds to the number of objects created below
        cls.num_forms_default = 2
        cls.num_questions_default = 5

        cls.form1 = FormFactory.create()
        cls.form2 = FormFactory.create()
        cls.form1_questions = [
            QuestionFactory.create(form_id=cls.form1, display_order=i) for i in range(5)
        ]

    def test_get_all_forms(self):
        response = self.client.get(reverse("forms-list"))
        forms = Form.objects.all()
        serializer = FormSerializer(forms, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_individual_form(self):
        response = self.client.get(reverse("forms-detail", args=[1]))
        form1 = Form.objects.get(id=1)
        serializer = FormSerializer(form1)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_form_with_questions_success(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 2,
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                },
                {
                    "display_order": 3,
                    "question": "question 3",
                    "question_type": "CHECKBOX",
                    "choices": [
                        {"choice_id": 1, "choice": "option1"},
                        {"choice_id": 2, "choice": "option2"},
                        {"choice_id": 3, "choice": "option3"},
                    ],
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Form.objects.count(), self.num_forms_default + 1)
        self.assertEqual(Question.objects.count(), self.num_questions_default + 3)

    def test_post_form_zero_questions_success(self):
        data = {"title": "test form", "questions": []}
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Form.objects.count(), self.num_forms_default + 1)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_missing_questions_field_failure(self):
        data = {"title": "test form"}
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_questions_not_in_running_display_order_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 3,  # wrong display_order
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.INVALID_DISPLAY_ORDER_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_questions_display_order_contains_zero_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 0,  # should start from 1
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 1,
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.INVALID_DISPLAY_ORDER_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_choices_not_in_running_order_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 1, "choice": "no"},  # invalid choice_id
                    ],
                },
                {
                    "display_order": 2,
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                },
                {
                    "display_order": 3,
                    "question": "question 3",
                    "question_type": "CHECKBOX",
                    "choices": [
                        {"choice_id": 1, "choice": "option1"},
                        {"choice_id": 2, "choice": "option2"},
                        {"choice_id": 3, "choice": "option3"},
                    ],
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.INVALID_CHOICE_ID_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_textbox_question_type_with_choices_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 2,
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"}
                    ],  # textbox questions should not have choices
                },
                {
                    "display_order": 3,
                    "question": "question 3",
                    "question_type": "CHECKBOX",
                    "choices": [
                        {"choice_id": 1, "choice": "option1"},
                        {"choice_id": 2, "choice": "option2"},
                        {"choice_id": 3, "choice": "option3"},
                    ],
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.INVALID_QUESTION_TYPE_WITH_CHOICES_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_radio_question_type_without_choices_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [],
                }
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.NO_CHOICES_SPECIFIED_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_checkbox_question_type_without_choices_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "CHECKBOX",
                }
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            FormSerializer.NO_CHOICES_SPECIFIED_MESSAGE,
        )
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_questions_missing_display_order_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "question": "question 2",
                    "question_type": "TEXTBOX",
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_questions_missing_question_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 2,
                    "question_type": "TEXTBOX",
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_questions_missing_question_type_failure(self):
        data = {
            "title": "test form",
            "questions": [
                {
                    "display_order": 1,
                    "question": "question 1",
                    "question_type": "RADIO",
                    "choices": [
                        {"choice_id": 1, "choice": "yes"},
                        {"choice_id": 2, "choice": "no"},
                    ],
                },
                {
                    "display_order": 2,
                    "question": "question 2",
                },
            ],
        }
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)

    def test_post_form_missing_title_field_failure(self):
        data = {"questions": []}
        response = self.client.post(
            reverse("forms-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)
