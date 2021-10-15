from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .serializers import (
    FormSerializer,
    SubmissionReadSerializer,
    SubmissionWriteSerializer,
)
from .models import Form, Submission


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all().order_by("id")
    http_method_names = ["get", "post", "put", "head"]
    serializer_class = FormSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by("form_id")
    http_method_names = ["get", "post", "put", "head"]

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST":
            return SubmissionWriteSerializer
        else:
            return SubmissionReadSerializer
