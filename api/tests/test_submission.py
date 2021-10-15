from api.models import Answer, Form, Question, Submission
from api.serializers import (
    AnswerSerializer,
    SubmissionReadSerializer,
    SubmissionWriteSerializer,
)
from django.test import TestCase
from django.urls import reverse
from factory import Faker
from rest_framework import status
from .factory import AnswerFactory, FormFactory, QuestionFactory, SubmissionFactory


class SubmissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup 1 form of 3 questions, with 2 sets of submissions and answers
        cls.question_types = ["radio", "checkbox", "textbox"]
        cls.num_questions_default = len(cls.question_types)
        cls.num_forms_default = 2
        cls.num_submissions_default = 2
        cls.num_answers_default = (
            cls.num_questions_default * cls.num_submissions_default
        )

        cls.form1 = FormFactory.create()
        cls.form2 = FormFactory.create()
        cls.questions = [
            QuestionFactory.create(
                form_id=cls.form1, display_order=i, question_type=cls.question_types[i]
            )
            for i in range(cls.num_questions_default)
        ]

        cls.submission1 = SubmissionFactory(form_id=cls.form1)
        cls.submission2 = SubmissionFactory(form_id=cls.form1)
        cls.answers1 = [
            AnswerFactory.create(
                submission_id=cls.submission1, question_id=cls.questions[i]
            )
            for i in range(cls.num_questions_default)
        ]
        cls.answers2 = [
            AnswerFactory.create(
                submission_id=cls.submission2, question_id=cls.questions[i]
            )
            for i in range(cls.num_questions_default)
        ]

    def test_get_all_submissions(self):
        response = self.client.get(reverse("submissions-list"))
        submissions = Submission.objects.all()
        serializer = SubmissionReadSerializer(submissions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_individual_submission(self):
        response = self.client.get(reverse("submissions-detail", args=[1]))
        submission1 = Submission.objects.get(id=1)
        serializer = SubmissionReadSerializer(submission1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_submissions_success(self):
        data = {
            "form_id": self.form1.id,
            "answers": [
                {"answer": "2", "question_type": self.question_types[0]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }
        response = self.client.post(
            reverse("submissions-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)
        self.assertEqual(Submission.objects.count(), self.num_submissions_default + 1)
        self.assertEqual(Answer.objects.count(), self.num_answers_default + 3)

    def test_post_missing_form_id_failure(self):
        data = {
            "answers": [
                {"answer": "2", "question_type": self.question_types[0]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }
        response = self.client.post(
            reverse("submissions-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            SubmissionWriteSerializer.FORM_ID_NOT_SPECIFIED_MESSAGE,
        )
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)

    def test_post_answers_with_wrong_question_type_failure(self):
        assert self.question_types[0] != self.question_types[1]
        data = {
            "form_id": self.form1.id,
            "answers": [
                # wrong question 1 type
                {"answer": "2", "question_type": self.question_types[1]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }

        response = self.client.post(
            reverse("submissions-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            SubmissionWriteSerializer.INVALID_QUESTION_TYPE_MATCH_MESSAGE,
        )
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)

    def test_post_different_answer_and_question_length_failure(self):
        assert self.num_questions_default != 2
        data = {
            "form_id": self.form1.id,
            "answers": [
                {"answer": "2", "question_type": self.question_types[0]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
            ],
        }

        response = self.client.post(
            reverse("submissions-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            SubmissionWriteSerializer.INVALID_ANSWERS_LENGTH_MESSAGE,
        )
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)

    def test_post_invalid_question_type_failure(self):
        assert self.question_types[0] != "invalid"
        data = {
            "form_id": self.form1.id,
            "answers": [
                {"answer": "2", "question_type": "invalid"},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }

        response = self.client.post(
            reverse("submissions-list"), data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            SubmissionWriteSerializer.INVALID_QUESTION_TYPE_MESSAGE,
        )
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)

    def test_put_submission_success(self):
        data = {
            "answers": [
                {"answer": "2", "question_type": self.question_types[0]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }

        # Assert that answers are initially the same
        self.assertEqual(
            AnswerSerializer(self.answers1, many=True).data,
            SubmissionReadSerializer(self.submission1).data["answers"],
        )
        response = self.client.put(
            reverse("submissions-detail", args=[1]),
            data,
            content_type="application/json",
        )

        # After PUT request, object counts remain the same, but answers are no longer the same
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)
        self.assertNotEqual(
            AnswerSerializer(self.answers1, many=True).data,
            SubmissionReadSerializer(self.submission1).data["answers"],
        )

    def test_put_submission_ignores_given_form_id_success(self):
        data = {
            "form_id": 2,  # not the same form as the one belonging to the submission of the PUT request below
            "answers": [
                {"answer": "2", "question_type": self.question_types[0]},
                {"answer": "1,3,4", "question_type": self.question_types[1]},
                {"answer": "text answer", "question_type": self.question_types[2]},
            ],
        }

        # Assert that answers are initially the same
        self.assertEqual(
            AnswerSerializer(self.answers2, many=True).data,
            SubmissionReadSerializer(self.submission2).data["answers"],
        )
        response = self.client.put(
            reverse("submissions-detail", args=[1]),
            data,
            content_type="application/json",
        )

        # After PUT request, the answers in the given form_id does not change, as the
        # wrongly specified form_id field is ignored
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Form.objects.count(), self.num_forms_default)
        self.assertEqual(Question.objects.count(), self.num_questions_default)
        self.assertEqual(Submission.objects.count(), self.num_submissions_default)
        self.assertEqual(Answer.objects.count(), self.num_answers_default)
        self.assertEqual(
            AnswerSerializer(self.answers2, many=True).data,
            SubmissionReadSerializer(self.submission2).data["answers"],
        )
