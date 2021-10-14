from django.db import models
from . import Question


class Choice(models.Model):
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )

    choice_id = models.IntegerField()
    choice = models.TextField()
