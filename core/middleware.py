from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from .models import Auditoria
import json

User = get_user_model()


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware para capturar automaticamente ações dos usuários para auditoria
    """
    
    def process_request(self, request):
        # Armazena informações da requisição para uso posterior
        request._audit_info = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'path': request.path,
            'method': request.method,
        }
    
    def get_client_ip(self, request):
        """Obtém o IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def log_audit(self, request, acao, objeto, objeto_id=None, detalhes=None):
        """Registra uma ação de auditoria"""
        if not request.user.is_authenticated:
            return
            
        try:
            Auditoria.objects.create(
                usuario=request.user,
                acao=acao,
                objeto=objeto,
                objeto_id=objeto_id,
                detalhes=detalhes,
                ip_address=request._audit_info.get('ip_address'),
                user_agent=request._audit_info.get('user_agent')
            )
        except Exception as e:
            # Log do erro sem quebrar a aplicação
            print(f"Erro ao registrar auditoria: {e}")


def audit_action(action, object_name, object_id=None, details=None):
    """
    Decorator para registrar ações de auditoria em views
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Executa a view
            response = view_func(request, *args, **kwargs)
            
            # Registra a auditoria se o usuário estiver autenticado
            if hasattr(request, '_audit_info') and request.user.is_authenticated:
                middleware = AuditMiddleware()
                middleware.log_audit(request, action, object_name, object_id, details)
            
            return response
        return wrapper
    return decorator
