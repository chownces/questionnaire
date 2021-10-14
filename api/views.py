from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .serializers import (
    FormSerializer,
    SubmissionReadSerializer,
    SubmissionWriteSerializer,
)
from .models import Form, Submission


class FormViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Form.objects.all().order_by("id")
    serializer_class = FormSerializer


class SubmissionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Submission.objects.all().order_by("form_id")

    def get_serializer_class(self):
        method = self.request.method
        if method == "PUT" or method == "POST":
            return SubmissionWriteSerializer
        else:
            return SubmissionReadSerializer
