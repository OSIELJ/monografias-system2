from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Monografia, Coorientador
from .forms import MonografiaForm
from .decorators import require_user_type, can_edit_monografia, can_view_monografia
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Monografia



# === Dashboard com estatísticas ===
@login_required
def dashboard(request):
    user = request.user

    # Filtragem conforme o tipo de usuário
    if getattr(user, "tipo_usuario", None) == "ALUNO":
        monografias = Monografia.objects.filter(autor__email=user.email)
    elif getattr(user, "tipo_usuario", None) == "PROF":
        monografias = Monografia.objects.filter(
            models.Q(orientador__usuario__email=user.email) |
            models.Q(coorientador__usuario__email=user.email)
        )
    else:
        monografias = Monografia.objects.all()

    # Estatísticas gerais
    total_monografias = monografias.count()
    monografias_em_andamento = monografias.filter(status='EM_ANDAMENTO').count()
    monografias_submetidas = monografias.filter(status='SUBMETIDA').count()
    monografias_aprovadas = monografias.filter(status='APROVADA').count()
    monografias_reprovadas = monografias.filter(status='REPROVADA').count()

    # Monografias recentes (últimas 5)
    monografias_recentes = monografias.order_by('-criado_em')[:5]

    # Estatísticas por status
    status_stats = {
        'EM_ANDAMENTO': monografias_em_andamento,
        'SUBMETIDA': monografias_submetidas,
        'APROVADA': monografias_aprovadas,
        'REPROVADA': monografias_reprovadas,
    }

    # Se for administrador, mostrar estatísticas gerais do sistema
    if user.is_superuser:
        from accounts.models import Usuario
        from .models import Aluno, Orientador, Coorientador
        
        total_usuarios = Usuario.objects.count()
        total_alunos = Aluno.objects.count()
        total_orientadores = Orientador.objects.count()
        total_coorientadores = Coorientador.objects.count()
        
        admin_stats = {
            'total_usuarios': total_usuarios,
            'total_alunos': total_alunos,
            'total_orientadores': total_orientadores,
            'total_coorientadores': total_coorientadores,
        }
    else:
        admin_stats = None

    context = {
        'monografias': monografias_recentes,
        'total_monografias': total_monografias,
        'status_stats': status_stats,
        'admin_stats': admin_stats,
        'user_type': getattr(user, "tipo_usuario", None),
    }

    return render(request, "core/dashboard.html", context)


# === Listagem com busca e paginação ===
@login_required
def monografia_list(request):
    user = request.user

    # Restringe a visualização conforme o tipo de usuário
    if getattr(user, "tipo_usuario", None) == "ALUNO":
        monografias = Monografia.objects.filter(autor__email=user.email)

    elif getattr(user, "tipo_usuario", None) == "PROF":
        monografias = Monografia.objects.filter(
            models.Q(orientador__usuario__email=user.email) |
            models.Q(coorientador__usuario__email=user.email)
        )

    else:
        monografias = Monografia.objects.all()

    # Implementar busca
    search_query = request.GET.get('search', '')
    if search_query:
        monografias = monografias.filter(
            Q(titulo__icontains=search_query) |
            Q(autor__nome__icontains=search_query) |
            Q(orientador__usuario__first_name__icontains=search_query) |
            Q(orientador__usuario__last_name__icontains=search_query) |
            Q(coorientador__usuario__first_name__icontains=search_query) |
            Q(coorientador__usuario__last_name__icontains=search_query) |
            Q(palavras_chave__icontains=search_query) |
            Q(resumo__icontains=search_query) |
            Q(abstract__icontains=search_query)
        )

    # Implementar filtros
    status_filter = request.GET.get('status', '')
    if status_filter:
        monografias = monografias.filter(status=status_filter)

    orientador_filter = request.GET.get('orientador', '')
    if orientador_filter:
        monografias = monografias.filter(
            Q(orientador__usuario__first_name__icontains=orientador_filter) |
            Q(orientador__usuario__last_name__icontains=orientador_filter)
        )

    # Implementar ordenação
    order_by = request.GET.get('order_by', '-criado_em')
    if order_by in ['titulo', '-titulo', 'criado_em', '-criado_em', 'data_defesa', '-data_defesa']:
        monografias = monografias.order_by(order_by)

    # Implementar paginação
    paginator = Paginator(monografias, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'monografias': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'orientador_filter': orientador_filter,
        'order_by': order_by,
        'status_choices': Monografia.STATUS_CHOICES,
    }

    return render(request, "core/monografia_list.html", context)


# === Criação ===
@login_required
@require_user_type('PROF', 'ALUNO')
def monografia_create(request):

    if request.method == "POST":
        form = MonografiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Monografia cadastrada com sucesso!")
            return redirect("monografia_list")
    else:
        form = MonografiaForm()

    return render(request, "core/monografia_form.html", {"form": form})


# === Edição ===
@login_required
@can_edit_monografia
def monografia_edit(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)

    form = MonografiaForm(request.POST or None, request.FILES or None, instance=monografia)
    if form.is_valid():
        form.save()
        messages.success(request, "Monografia atualizada com sucesso!")
        return redirect("monografia_list")

    return render(request, "core/monografia_form.html", {"form": form, "monografia": monografia})


# === Exclusão ===
@login_required
@require_user_type('ADMIN')
def monografia_delete(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)

    if request.method == "POST":
        monografia.delete()
        messages.success(request, "Monografia excluída com sucesso!")
        return redirect("monografia_list")

    return render(request, "core/monografia_confirm_delete.html", {"monografia": monografia})


# === Visualização de detalhes ===
@login_required
@can_view_monografia
def monografia_detail(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)
    return render(request, "core/monografia_detail.html", {"monografia": monografia})


# Seu views.py


def baixar_pdf(request, pk):
    # 1. Busca a monografia pelo ID
    monografia = get_object_or_404(Monografia, pk=pk)
    
    # 2. Obtém os dados binários. 
    # **IMPORTANTE**: Substitua 'arquivo_pdf_binario' pelo nome exato do seu BinaryField no modelo Monografia.
    dados_pdf = monografia.arquivo_pdf 
    
    if not dados_pdf:
        # Lida com o caso onde o campo BinaryField está vazio/nulo
        raise Http404("O arquivo PDF não foi encontrado para esta monografia.")

    # 3. Configura o HttpResponse para enviar dados binários de PDF
    response = HttpResponse(dados_pdf, content_type='application/pdf')
    
    # 4. Define o cabeçalho para forçar o download e nomear o arquivo
    nome_arquivo = f"monografia_{monografia.pk}.pdf" # Extensão .pdf
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    
    return response


# === View para AJAX - obter coorientadores ===
@login_required
def get_coorientadores(request):
    orientador_id = request.GET.get('orientador_id')
    
    if orientador_id:
        try:
            from .models import Orientador
            orientador = Orientador.objects.get(id=orientador_id)
            # Excluir o orientador selecionado da lista de coorientadores
            coorientadores = Coorientador.objects.exclude(usuario=orientador.usuario)
        except Orientador.DoesNotExist:
            coorientadores = Coorientador.objects.all()
    else:
        coorientadores = Coorientador.objects.all()
    
    data = []
    for coorientador in coorientadores:
        data.append({
            'id': coorientador.id,
            'nome': str(coorientador),
        })
    
    return JsonResponse(data, safe=False)