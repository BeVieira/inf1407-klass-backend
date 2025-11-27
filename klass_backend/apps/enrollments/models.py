from django.conf import settings
from django.db import models

from apps.courses.models import Section

class Enrollment(models.Model):
  student = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="enrollments",
  )
  section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrollments")
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ("student", "section")

  def __str__(self):
    return f"{self.student} -> {self.section}"