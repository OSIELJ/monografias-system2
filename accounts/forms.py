from django import forms
from allauth.account.forms import SignupForm

from core.models import Aluno, Orientador

class CustomSignupForm(SignupForm):
    TIPO_USUARIO_CHOICES = [
        ("ALUNO", "Aluno"),
        ("PROF", "Professor"),
    ]

    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        label="Tipo de Usuário",
        required=True,
    )

    def save(self, request):
        user = super().save(request)
        user.tipo_usuario = self.cleaned_data["tipo_usuario"]
        user.save()
        if user.tipo_usuario == 'ALUNO':
            Aluno.objects.create(
            nome=f"{user.username} ",
            matricula=f"MATR-{user.id:05d}",
            email=user.email
         )
        elif user.tipo_usuario == 'PROF':
            Orientador.objects.create(
                usuario=user,
                titulacao="Mestre",
                area_pesquisa="A definir"
            )

        return user
