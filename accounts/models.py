from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('PROF', 'Professor'),
        ('ALUNO', 'Aluno'),
    ]

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPOS_USUARIO,
        default='ALUNO',
    )

    # Campos opcionais extras
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"
