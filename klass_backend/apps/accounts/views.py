from rest_framework import viewsets, status, generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import User
from .serializers import (
    UserSerializer, ChangePasswordSerializer, 
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_permissions(self):
    if self.action in ['create']:
      return [AllowAny()]  # qualquer um pode criar conta
    return [IsAuthenticated()]  # listar / atualizar / deletar precisa estar logado

class ChangePasswordView(generics.GenericAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = ChangePasswordSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    if not user.check_password(serializer.data.get("old_password")):
      return Response(
        {"old_password": ["Senha antiga incorreta."]}, 
        status=status.HTTP_400_BAD_REQUEST
      )

    user.set_password(serializer.data.get("new_password"))
    user.save()
    return Response({"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)

class PasswordResetRequestView(views.APIView):
  permission_classes = [AllowAny]
  serializer_class = PasswordResetRequestSerializer

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      # Por segurança, não informamos se o email existe ou não
      return Response(
        {"detail": "Se um usuário com este email existir, um link de redefinição foi enviado."},
        status=status.HTTP_200_OK
      )

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # URL do Frontend (Placeholder por enquanto, ajustável via ENV ou hardcoded)
    # Ex: http://localhost:3000/reset-password/uid/token
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    reset_link = f"{frontend_url}/reset-password/{uid}/{token}"

    html_message = render_to_string('emails/password_reset.html', {'reset_link': reset_link})
    plain_message = strip_tags(html_message)

    send_mail(
      subject='Redefinição de Senha - Klass',
      message=plain_message,
      from_email=settings.DEFAULT_FROM_EMAIL,
      recipient_list=[email],
      html_message=html_message,
      fail_silently=False,
    )

    return Response(
      {"detail": "Se um usuário com este email existir, um link de redefinição foi enviado."},
      status=status.HTTP_200_OK
    )

class PasswordResetConfirmView(generics.GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = PasswordResetConfirmSerializer

  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
  
class AuthMeView(views.APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
