from django import forms
from allauth.account.forms import SignupForm

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
        return user
