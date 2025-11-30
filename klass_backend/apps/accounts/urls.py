from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ChangePasswordView, 
    PasswordResetRequestView, PasswordResetConfirmView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
  path('', include(router.urls)),
  path('change-password/', ChangePasswordView.as_view(), name='change-password'),
  path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
  path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]