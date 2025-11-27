from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsStudent, IsTeacherOrAdmin
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
  queryset = Enrollment.objects.select_related("student", "section", "section__course")
  serializer_class = EnrollmentSerializer
  permission_classes = [IsAuthenticated]

  def get_permissions(self):
    if self.action == "create":
      return [IsAuthenticated(), IsStudent()]
    if self.action == "my":
      return [IsAuthenticated(), IsStudent()]
    if self.action in ["list", "retrieve"]:
      return [IsAuthenticated(), IsTeacherOrAdmin()]
    if self.action == "destroy":
      return [IsAuthenticated()]
    return super().get_permissions()

  def get_queryset(self):
    if self.action == "list":
      return Enrollment.objects.select_related("student", "section", "section__course")
    if self.action == "my":
      return Enrollment.objects.filter(student=self.request.user).select_related(
        "section", "section__course"
      )
    return super().get_queryset()

  def perform_destroy(self, instance):
    user = self.request.user
    if user.role == "student" and instance.student != user:
      raise PermissionDenied("O aluno só pode cancelar a própria matrícula.")
    if user.role not in ["student", "admin"]:
      raise PermissionDenied("Ação permitida apenas para alunos ou admins.")
    instance.delete()

  @extend_schema(description="Lista matrículas do próprio aluno")
  @action(detail=False, methods=["get"], url_path="my")
  def my(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  @extend_schema(description="Cria uma matrícula para o aluno autenticado")
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)

  @extend_schema(description="Lista matrículas (somente professores e admins)")
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

  @extend_schema(description="Remove uma matrícula (aluno dono ou admin)")
  def destroy(self, request, *args, **kwargs):
    return super().destroy(request, *args, **kwargs)