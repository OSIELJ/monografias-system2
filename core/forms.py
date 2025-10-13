from django import forms
from django.core.exceptions import ValidationError
from .models import Monografia, Aluno, Orientador, Coorientador

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
            "data_defesa": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "resumo": forms.Textarea(attrs={"rows": 3, "placeholder": "Digite o resumo da monografia em português...", "class": "form-control"}),
            "abstract": forms.Textarea(attrs={"rows": 3, "placeholder": "Digite o abstract da monografia em inglês...", "class": "form-control"}),
            "palavras_chave": forms.TextInput(attrs={"placeholder": "Ex: inteligência artificial, machine learning, redes neurais", "class": "form-control"}),
            "titulo": forms.TextInput(attrs={"placeholder": "Digite o título da monografia...", "class": "form-control"}),
            "autor": forms.Select(attrs={"class": "form-control"}),
            "orientador": forms.Select(attrs={"class": "form-control"}),
            "coorientador": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "arquivo_pdf": forms.FileInput(attrs={"class": "form-control", "accept": ".pdf"}),
        }
        labels = {
            "titulo": "📝 Título da Monografia",
            "resumo": "📄 Resumo (Português)",
            "abstract": "🌍 Abstract (Inglês)",
            "palavras_chave": "🏷️ Palavras-chave",
            "status": "📊 Status",
            "data_defesa": "📅 Data da Defesa",
            "arquivo_pdf": "📎 Arquivo PDF",
            "autor": "👨‍🎓 Autor (Aluno)",
            "orientador": "👨‍🏫 Orientador",
            "coorientador": "👨‍🏫 Coorientador",
        }
        help_texts = {
            "titulo": "Digite o título completo da monografia (mínimo 10 caracteres)",
            "resumo": "Resumo em português da monografia (mínimo 100 caracteres)",
            "abstract": "Abstract em inglês da monografia (opcional, mas recomendado)",
            "palavras_chave": "Digite as palavras-chave separadas por vírgula (mínimo 3 palavras)",
            "data_defesa": "Selecione a data prevista para a defesa da monografia",
            "arquivo_pdf": "Faça upload do arquivo PDF da monografia (máximo 10MB)",
            "autor": "Selecione o aluno autor da monografia",
            "orientador": "Selecione o professor orientador (obrigatório)",
            "coorientador": "Selecione o professor coorientador (opcional)",
            "status": "Selecione o status atual da monografia",
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if titulo:
            if len(titulo.strip()) < 10:
                raise ValidationError("O título deve ter pelo menos 10 caracteres.")
            if len(titulo) > 200:
                raise ValidationError("O título deve ter no máximo 200 caracteres.")
        return titulo

    def clean_resumo(self):
        resumo = self.cleaned_data.get('resumo')
        if resumo:
            if len(resumo.strip()) < 100:
                raise ValidationError("O resumo deve ter pelo menos 100 caracteres.")
            if len(resumo) > 2000:
                raise ValidationError("O resumo deve ter no máximo 2000 caracteres.")
        return resumo

    def clean_abstract(self):
        abstract = self.cleaned_data.get('abstract')
        if abstract and len(abstract.strip()) < 50:
            raise ValidationError("O abstract deve ter pelo menos 50 caracteres.")
        return abstract

    def clean_palavras_chave(self):
        palavras_chave = self.cleaned_data.get('palavras_chave')
        if palavras_chave:
            # Verificar se há pelo menos 3 palavras-chave
            palavras = [p.strip() for p in palavras_chave.split(',') if p.strip()]
            if len(palavras) < 3:
                raise ValidationError("Digite pelo menos 3 palavras-chave separadas por vírgula.")
            
            # Verificar se cada palavra-chave tem pelo menos 3 caracteres
            for palavra in palavras:
                if len(palavra) < 3:
                    raise ValidationError("Cada palavra-chave deve ter pelo menos 3 caracteres.")
        return palavras_chave

    def clean_data_defesa(self):
        data_defesa = self.cleaned_data.get('data_defesa')
        if data_defesa:
            from django.utils import timezone
            if data_defesa < timezone.now().date():
                raise ValidationError("A data da defesa não pode ser no passado.")
        return data_defesa

    def clean(self):
        cleaned_data = super().clean()
        orientador = cleaned_data.get('orientador')
        coorientador = cleaned_data.get('coorientador')
        
        # Verificar se orientador e coorientador são diferentes
        if orientador and coorientador and orientador == coorientador:
            raise ValidationError("O orientador e coorientador devem ser pessoas diferentes.")
        
        return cleaned_data


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email']
        labels = {
            'nome': 'Nome Completo',
            'matricula': 'Matrícula',
            'email': 'E-mail',
        }
        help_texts = {
            'nome': 'Digite o nome completo do aluno',
            'matricula': 'Número da matrícula (único)',
            'email': 'E-mail válido e único',
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome:
            if len(nome.strip()) < 5:
                raise ValidationError("O nome deve ter pelo menos 5 caracteres.")
            # Verificar se contém apenas letras e espaços
            if not all(c.isalpha() or c.isspace() for c in nome):
                raise ValidationError("O nome deve conter apenas letras e espaços.")
        return nome

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if matricula:
            if len(matricula) < 5:
                raise ValidationError("A matrícula deve ter pelo menos 5 caracteres.")
            # Verificar se contém apenas números e letras
            if not matricula.isalnum():
                raise ValidationError("A matrícula deve conter apenas números e letras.")
        return matricula


class OrientadorForm(forms.ModelForm):
    class Meta:
        model = Orientador
        fields = ['usuario', 'titulacao', 'area_pesquisa']
        labels = {
            'usuario': 'Usuário (Professor)',
            'titulacao': 'Titulação',
            'area_pesquisa': 'Área de Pesquisa',
        }
        help_texts = {
            'titulacao': 'Ex: Doutor, Mestre, Especialista',
            'area_pesquisa': 'Área de atuação do orientador',
        }

    def clean_titulacao(self):
        titulacao = self.cleaned_data.get('titulacao')
        if titulacao and len(titulacao.strip()) < 3:
            raise ValidationError("A titulação deve ter pelo menos 3 caracteres.")
        return titulacao

    def clean_area_pesquisa(self):
        area_pesquisa = self.cleaned_data.get('area_pesquisa')
        if area_pesquisa and len(area_pesquisa.strip()) < 5:
            raise ValidationError("A área de pesquisa deve ter pelo menos 5 caracteres.")
        return area_pesquisa
