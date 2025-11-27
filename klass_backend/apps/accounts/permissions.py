from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated and request.user.role == "student")


class IsTeacher(BasePermission):
  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated and request.user.role == "teacher")


class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated and request.user.role == "admin")


class IsTeacherOrAdmin(BasePermission):
  def has_permission(self, request, view):
    return bool(
      request.user
      and request.user.is_authenticated
      and request.user.role in ["teacher", "admin"]
    )


class IsOwnerOrAdmin(BasePermission):
  def has_object_permission(self, request, view, obj):
    if not request.user or not request.user.is_authenticated:
      return False
    if request.user.role == "admin":
      return True
    return getattr(obj, "owner", None) == request.user

  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated)