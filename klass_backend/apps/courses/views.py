from django.shortcuts import render
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.accounts.permissions import IsOwnerOrAdmin, IsTeacherOrAdmin
from .models import Course, Section
from .serializers import CourseSerializer, SectionSerializer
class CourseViewSet(viewsets.ModelViewSet):
  queryset = Course.objects.all().order_by("-created_at")
  serializer_class = CourseSerializer

  def get_permissions(self):
    if self.action in ["list", "retrieve"]:
      return [AllowAny()]
    if self.action == "create":
      return [IsAuthenticated(), IsTeacherOrAdmin()]
    return [IsOwnerOrAdmin()]

  def perform_create(self, serializer):
    serializer.save()

  @extend_schema(
    description="Lista todos os cursos",
    parameters=[OpenApiParameter("search", str, OpenApiParameter.QUERY, description="Filtro opcional")],
  )
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

  @extend_schema(description="Cria um novo curso (apenas professores ou administradores)")
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)

  @extend_schema(description="Obtém detalhes de um curso")
  def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)

  @extend_schema(description="Atualiza um curso (somente o dono ou admin)")
  def update(self, request, *args, **kwargs):
    return super().update(request, *args, **kwargs)

  @extend_schema(description="Atualização parcial de um curso (somente o dono ou admin)")
  def partial_update(self, request, *args, **kwargs):
    return super().partial_update(request, *args, **kwargs)

  @extend_schema(description="Remove um curso (somente o dono ou admin)")
  def destroy(self, request, *args, **kwargs):
    return super().destroy(request, *args, **kwargs)


class SectionViewSet(viewsets.ModelViewSet):
  queryset = Section.objects.select_related("course", "course__owner").all().order_by("-created_at")
  serializer_class = SectionSerializer
  permission_classes = [IsAuthenticated]

  def get_permissions(self):
    if self.action in ["list", "retrieve"]:
      return [IsAuthenticated()]
    return [IsAuthenticated(), IsTeacherOrAdmin()]

  def perform_create(self, serializer):
    user = self.request.user
    course = serializer.validated_data.get("course")
    if user.role != "admin" and course.owner != user:
      raise PermissionDenied("Apenas o professor dono do curso ou admin pode criar turmas.")
    serializer.save()

  def perform_update(self, serializer):
    course = serializer.validated_data.get("course", self.get_object().course)
    self._ensure_owner_or_admin(course)
    serializer.save()

  def perform_destroy(self, instance):
    self._ensure_owner_or_admin(instance.course)
    instance.delete()

  def _ensure_owner_or_admin(self, course):
    user = self.request.user
    if user.role != "admin" and course.owner != user:
      raise PermissionDenied("Apenas o professor dono do curso ou admin pode modificar turmas.")

  @extend_schema(description="Lista todas as turmas (somente usuários autenticados)")
  def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)

  @extend_schema(description="Cria uma nova turma para um curso")
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)

  @extend_schema(description="Detalhes de uma turma")
  def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)

  @extend_schema(description="Atualiza uma turma (somente professor dono ou admin)")
  def update(self, request, *args, **kwargs):
    return super().update(request, *args, **kwargs)

  @extend_schema(description="Atualização parcial de uma turma")
  def partial_update(self, request, *args, **kwargs):
    return super().partial_update(request, *args, **kwargs)

  @extend_schema(description="Remove uma turma (somente professor dono ou admin)")
  def destroy(self, request, *args, **kwargs):
    return super().destroy(request, *args, **kwargs)