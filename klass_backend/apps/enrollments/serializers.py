from rest_framework import serializers

from apps.courses.models import Section
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
  student = serializers.PrimaryKeyRelatedField(read_only=True)
  section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

  class Meta:
    model = Enrollment
    fields = ["id", "student", "section", "created_at"]
    read_only_fields = ["id", "created_at", "student"]

  def validate(self, attrs):
    request = self.context.get("request")
    user = getattr(request, "user", None)
    section = attrs.get("section")

    if not user or not user.is_authenticated:
      raise serializers.ValidationError("Usuário não autenticado.")

    if user.role != "student":
      raise serializers.ValidationError("Somente alunos podem se matricular.")

    if section.enrollments.filter(student=user).exists():
      raise serializers.ValidationError("O aluno já está matriculado nesta turma.")

    if section.enrollments.count() >= section.vacancies:
      raise serializers.ValidationError("Não há vagas disponíveis nesta turma.")

    attrs["student"] = user
    return attrs

  def create(self, validated_data):
    validated_data["student"] = validated_data.get("student")
    return super().create(validated_data)