from django.db import models
from . import Form


class Submission(models.Model):
    form_id = models.ForeignKey(
        Form, on_delete=models.CASCADE, related_name="submissions"
    )
