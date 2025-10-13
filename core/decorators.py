from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def require_user_type(*allowed_types):
    """
    Decorator para verificar se o usuário tem um tipo específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Você precisa estar logado.")
            
            user_type = getattr(request.user, 'tipo_usuario', None)
            if user_type not in allowed_types and not request.user.is_superuser:
                tipos_nomes = {
                    'PROF': 'Professor',
                    'ALUNO': 'Aluno', 
                    'ADMIN': 'Administrador'
                }
                tipos_permitidos = [tipos_nomes.get(t, t) for t in allowed_types]
                return HttpResponseForbidden(
                    f"Apenas usuários do tipo {', '.join(tipos_permitidos)} podem acessar esta página."
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_superuser(view_func):
    """
    Decorator para verificar se o usuário é superusuário
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Você precisa estar logado.")
        
        if not request.user.is_superuser:
            return HttpResponseForbidden("Apenas administradores podem acessar esta página.")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def can_edit_monografia(view_func):
    """
    Decorator para verificar se o usuário pode editar uma monografia específica
    """
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Você precisa estar logado.")
        
        # Superusuários podem editar qualquer monografia
        if request.user.is_superuser:
            return view_func(request, pk, *args, **kwargs)
        
        # Importar aqui para evitar import circular
        from .models import Monografia
        from django.shortcuts import get_object_or_404
        
        monografia = get_object_or_404(Monografia, pk=pk)
        user_type = getattr(request.user, 'tipo_usuario', None)
        
        if user_type == 'ALUNO':
            # Alunos não podem editar monografias
            return HttpResponseForbidden("Alunos não podem editar monografias.")
        
        elif user_type == 'PROF':
            # Professores só podem editar monografias que orientam
            if not (monografia.orientador and monografia.orientador.usuario.email == request.user.email) and \
               not (monografia.coorientador and monografia.coorientador.usuario.email == request.user.email):
                return HttpResponseForbidden("Você só pode editar monografias que orienta.")
        
        return view_func(request, pk, *args, **kwargs)
    return wrapper


def can_view_monografia(view_func):
    """
    Decorator para verificar se o usuário pode visualizar uma monografia específica
    """
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Você precisa estar logado.")
        
        # Superusuários podem ver qualquer monografia
        if request.user.is_superuser:
            return view_func(request, pk, *args, **kwargs)
        
        # Importar aqui para evitar import circular
        from .models import Monografia
        from django.shortcuts import get_object_or_404
        
        monografia = get_object_or_404(Monografia, pk=pk)
        user_type = getattr(request.user, 'tipo_usuario', None)
        
        if user_type == 'ALUNO':
            # Alunos só podem ver suas próprias monografias
            if monografia.autor.email != request.user.email:
                return HttpResponseForbidden("Você só pode visualizar suas próprias monografias.")
        
        elif user_type == 'PROF':
            # Professores só podem ver monografias que orientam
            if not (monografia.orientador and monografia.orientador.usuario.email == request.user.email) and \
               not (monografia.coorientador and monografia.coorientador.usuario.email == request.user.email):
                return HttpResponseForbidden("Você só pode visualizar monografias que orienta.")
        
        return view_func(request, pk, *args, **kwargs)
    return wrapper
