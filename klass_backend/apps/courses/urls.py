from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, SectionViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"sections", SectionViewSet, basename="section")

urlpatterns = [path("", include(router.urls))]