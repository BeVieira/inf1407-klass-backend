from django.conf import settings
from django.db import models

class Course(models.Model):
  code = models.CharField(max_length=20, unique=True)
  name = models.CharField(max_length=150)
  description = models.TextField(blank=True)
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="courses",
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name


class Section(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
  days = models.CharField(max_length=20, blank=True)
  schedule = models.CharField(max_length=255)
  vacancies = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.course.name} - {self.days} {self.schedule}"