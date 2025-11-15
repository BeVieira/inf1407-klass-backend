from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_permissions(self):
    if self.action in ['create']:
      return [AllowAny()]  # qualquer um pode criar conta
    return [IsAuthenticated()]  # listar / atualizar / deletar precisa estar logado
