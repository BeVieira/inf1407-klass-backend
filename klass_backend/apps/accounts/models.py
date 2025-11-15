from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

  registration = models.CharField(
    max_length=10,
    unique=True,
    help_text="Matrícula do usuário. 7 dígitos para alunos. 5 dígitos para professores e admins."
  )

  role = models.CharField(
    max_length=20,
    editable=False,
  )

  def save(self, *args, **kwargs):
    self.assign_role_from_registration()
    super().save(*args, **kwargs)

  def assign_role_from_registration(self):
    reg = self.registration

    if len(reg) == 5 and reg.isdigit():
      if reg[0] == "0":
        self.role = "admin"
      else:
        self.role = "teacher"
    else:
      self.role = "student"

  def __str__(self):
    return f"{self.username} ({self.registration}) - {self.role}"