from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

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
    extra_kwargs = {
      'password': {'write_only': True},
    }

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    user = User(**validated_data)
    if password:
      user.set_password(password)
    else:
      user.set_unusable_password()
    user.save()
    return user

  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)
    if password:
      user.set_password(password)
      user.save(update_fields=['password'])
    return user

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

class ChangePasswordSerializer(serializers.Serializer):
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)

  def validate_new_password(self, value):
    validate_password(value)
    return value

class PasswordResetRequestSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
  new_password = serializers.CharField(required=True)
  token = serializers.CharField(required=True)
  uidb64 = serializers.CharField(required=True)

  def validate_new_password(self, value):
    validate_password(value)
    return value

  def validate(self, attrs):
    try:
      uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
      self.user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      raise serializers.ValidationError("Link de redefinição inválido.")

    if not default_token_generator.check_token(self.user, attrs['token']):
      raise serializers.ValidationError("Token inválido ou expirado.")

    return attrs

  def save(self):
    self.user.set_password(self.validated_data['new_password'])
    self.user.save()
    return self.user
