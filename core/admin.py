from django.contrib import admin
from django.utils.html import format_html
from .models import Aluno, Orientador, Coorientador, Monografia, Banca, Auditoria


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'matricula', 'email', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['nome', 'matricula', 'email']
    readonly_fields = ['criado_em']
    ordering = ['nome']


@admin.register(Orientador)
class OrientadorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulacao', 'area_pesquisa']
    list_filter = ['titulacao', 'area_pesquisa']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'area_pesquisa']
    ordering = ['usuario__first_name']


@admin.register(Coorientador)
class CoorientadorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'titulacao', 'area_pesquisa']
    list_filter = ['titulacao', 'area_pesquisa']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'area_pesquisa']
    ordering = ['usuario__first_name']


@admin.register(Monografia)
class MonografiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'orientador', 'status', 'data_defesa', 'criado_em']
    list_filter = ['status', 'criado_em', 'data_defesa', 'orientador', 'coorientador']
    search_fields = ['titulo', 'autor__nome', 'orientador__usuario__first_name', 'palavras_chave']
    readonly_fields = ['criado_em', 'atualizado_em']
    ordering = ['-criado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'autor', 'status', 'data_defesa')
        }),
        ('Conteúdo', {
            'fields': ('resumo', 'abstract', 'palavras_chave')
        }),
        ('Orientação', {
            'fields': ('orientador', 'coorientador')
        }),
        ('Arquivo', {
            'fields': ('arquivo_pdf',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('autor', 'orientador__usuario', 'coorientador__usuario')


@admin.register(Banca)
class BancaAdmin(admin.ModelAdmin):
    list_display = ['monografia', 'data_defesa', 'local_defesa', 'nota_final']
    list_filter = ['data_defesa', 'nota_final']
    search_fields = ['monografia__titulo', 'local_defesa']
    ordering = ['-data_defesa']
    
    filter_horizontal = ['avaliadores']


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'objeto', 'timestamp', 'ip_address']
    list_filter = ['acao', 'timestamp', 'objeto']
    search_fields = ['usuario__username', 'usuario__email', 'objeto', 'detalhes']
    readonly_fields = ['timestamp', 'ip_address', 'user_agent']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# Personalizar o título do admin
admin.site.site_header = "Sistema de Monografias - Administração"
admin.site.site_title = "Admin Monografias"
admin.site.index_title = "Painel de Administração"