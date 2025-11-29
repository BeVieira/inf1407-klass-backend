from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'id',
      'username',
      'email',
      'password',
      'registration',
      'role',
    ]
    read_only_fields = [
      'role',
    ]

  def validate_registration(self, value):
    if not value.isdigit():
      raise serializers.ValidationError("A matrícula deve conter apenas números.")

    if len(value) == 7:
      return value

    if len(value) == 5:
      return value

    raise serializers.ValidationError(
      "Matrícula inválida. Alunos usam 7 dígitos. Professores/Admin usam 5 dígitos."
    )
