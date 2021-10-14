from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    FormSerializer,
    SubmissionReadSerializer,
    SubmissionWriteSerializer,
)
from .models import Form, Submission


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all().order_by("id")
    serializer_class = FormSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by("form_id")

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST":
            return SubmissionWriteSerializer
        else:
            return SubmissionReadSerializer
