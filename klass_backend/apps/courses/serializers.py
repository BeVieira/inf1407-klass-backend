from rest_framework import serializers
from apps.accounts.models import User
from .models import Course, Section

class CourseSerializer(serializers.ModelSerializer):
  owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role="teacher"))

  class Meta:
    model = Course
    fields = ["id", "code", "name", "description", "owner", "created_at"]
    read_only_fields = ["id", "created_at"]

  def validate_owner(self, value):
    if value.role != "teacher":
      raise serializers.ValidationError("O responsável pelo curso deve ser um professor.")
    return value

  def create(self, validated_data):
    request = self.context.get("request")
    user = getattr(request, "user", None)
    if user and user.role == "teacher":
      validated_data["owner"] = user
    return super().create(validated_data)

  def update(self, instance, validated_data):
    # Evita alterar o dono para não-admins
    request = self.context.get("request")
    user = getattr(request, "user", None)
    if user and user.role != "admin":
      validated_data.pop("owner", None)
    return super().update(instance, validated_data)


class SectionSerializer(serializers.ModelSerializer):
  course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
  occupied_vacancies = serializers.IntegerField(read_only=True)

  class Meta:
    model = Section
    fields = [
      "id",
      "course",
      "days",
      "schedule",
      "vacancies",
      "occupied_vacancies",
      "created_at",
    ]
    read_only_fields = ["id", "occupied_vacancies", "created_at"]