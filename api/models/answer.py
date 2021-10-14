from django.db import models
from . import Question, Submission


class Answer(models.Model):
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )

    # NOTE: Answers are stored as text (regardless of question type) for a simplified implementation.
    # A future extension would be to store integers for Radio and Checkbox questions,
    # and text for textbox questions.
    answer = models.TextField()
    submission_id = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="answers"
    )
