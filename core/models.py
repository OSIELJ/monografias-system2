from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from accounts.models import Usuario  # Importa o modelo de usuário personalizado
from .validators import validate_pdf_file, validate_file_size


# MODELO: Aluno
class Aluno(models.Model):
    nome = models.CharField(max_length=120)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(default=timezone.now)
    historico = HistoricalRecords()

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


# MODELO: Orientador (vinculado ao Usuário do tipo PROFESSOR)
class Orientador(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'PROF'},
        related_name='perfil_orientador',
        null=True, blank=True
    )
    titulacao = models.CharField(max_length=100)
    area_pesquisa = models.CharField(max_length=120)
    historico = HistoricalRecords()

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.area_pesquisa}"


# MODELO: Coorientador (também apenas professores)
class Coorientador(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'PROF'},
        related_name='perfil_coorientador',
        null=True, blank=True
    )
    titulacao = models.CharField(max_length=100)
    area_pesquisa = models.CharField(max_length=120)
    historico = HistoricalRecords()

    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username} - {self.area_pesquisa}"


# MODELO: Monografia
class Monografia(models.Model):
    STATUS_CHOICES = [
        ('EM_ANDAMENTO', 'Em andamento'),
        ('SUBMETIDA', 'Submetida'),
        ('APROVADA', 'Aprovada'),
        ('REPROVADA', 'Reprovada'),
    ]

    titulo = models.CharField(max_length=200)
    resumo = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    palavras_chave = models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANDAMENTO')
    data_defesa = models.DateField(blank=True, null=True)
    arquivo_pdf = models.FileField(
        upload_to='monografias/', 
        blank=True, 
        null=True,
        validators=[validate_pdf_file, validate_file_size]
    )

    autor = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='monografias')
    orientador = models.ForeignKey(
        Orientador,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orientacoes'
    )
    coorientador = models.ForeignKey(
        Coorientador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coorientacoes'
    )

    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)
    historico = HistoricalRecords()

    def __str__(self):
        return self.titulo


# MODELO: Banca
class Banca(models.Model):
    monografia = models.OneToOneField(Monografia, on_delete=models.CASCADE, related_name='banca')
    avaliadores = models.ManyToManyField(Orientador, related_name='bancas')
    data_defesa = models.DateField()
    local_defesa = models.CharField(max_length=150)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    historico = HistoricalRecords()

    def __str__(self):
        return f"Banca de {self.monografia.titulo}"


# MODELO: Auditoria
class Auditoria(models.Model):
    TIPO_ACAO_CHOICES = [
        ('CREATE', 'Criação'),
        ('READ', 'Visualização'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='auditorias')
    acao = models.CharField(max_length=20, choices=TIPO_ACAO_CHOICES)
    objeto = models.CharField(max_length=100)  # Nome do objeto afetado (ex: "Monografia")
    objeto_id = models.PositiveIntegerField(null=True, blank=True)  # ID do objeto
    detalhes = models.TextField(blank=True, null=True)  # Detalhes adicionais
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'

    def __str__(self):
        return f"{self.usuario.username} - {self.get_acao_display()} - {self.objeto} ({self.timestamp})"