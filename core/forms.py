from django import forms
from .models import Monografia

class MonografiaForm(forms.ModelForm):
    class Meta:
        model = Monografia
        fields = [
            "titulo",
            "resumo",
            "abstract",
            "palavras_chave",
            "status",
            "data_defesa",
            "arquivo_pdf",
            "autor",
            "orientador",
            "coorientador",
        ]
        widgets = {
            "data_defesa": forms.DateInput(attrs={"type": "date"}),
            "resumo": forms.Textarea(attrs={"rows": 3}),
            "abstract": forms.Textarea(attrs={"rows": 3}),
        }
