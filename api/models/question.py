from django.db import models
from . import Form


class Question(models.Model):
    QuestionTypes = (
        ("textbox", "textbox"),
        ("checkbox", "checkbox"),
        ("radio", "radio"),
    )

    form_id = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="questions"
    )

    # The display order of the question in the form. One-indexed.
    display_order = models.IntegerField()

    question = models.TextField()
    question_type = models.CharField(max_length=20, choices=QuestionTypes)
