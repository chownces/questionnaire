from django.urls import include, path
from rest_framework import routers
from . import views

# NOTE: Using router to dynamically route requests with Viewsets to reduce boilerplate
# and to simplify this implementation.
# If we want to use standard DRF Views instead of Viewsets, we don't need a router
router = routers.SimpleRouter()
router.register(r"forms", views.FormViewSet, basename="forms")
router.register(r"submissions", views.SubmissionViewSet, basename="submissions")

urlpatterns = [
    path("", include(router.urls)),
]
