from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class PasswordComplexityValidator:
    """
    Validador personalizado para políticas de senha mais robustas
    """
    
    def __init__(self, min_length=8, require_uppercase=True, require_lowercase=True, 
                 require_digits=True, require_special_chars=True, 
                 forbidden_patterns=None):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special_chars = require_special_chars
        self.forbidden_patterns = forbidden_patterns or []
    
    def validate(self, password, user=None):
        errors = []
        
        # Verificar comprimento mínimo
        if len(password) < self.min_length:
            errors.append(
                ValidationError(
                    _("A senha deve ter pelo menos %(min_length)d caracteres."),
                    code='password_too_short',
                    params={'min_length': self.min_length},
                )
            )
        
        # Verificar maiúsculas
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos uma letra maiúscula."),
                    code='password_no_upper',
                )
            )
        
        # Verificar minúsculas
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos uma letra minúscula."),
                    code='password_no_lower',
                )
            )
        
        # Verificar dígitos
        if self.require_digits and not re.search(r'\d', password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos um número."),
                    code='password_no_digit',
                )
            )
        
        # Verificar caracteres especiais
        if self.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(
                ValidationError(
                    _("A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>)."),
                    code='password_no_special',
                )
            )
        
        # Verificar padrões proibidos
        for pattern in self.forbidden_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                errors.append(
                    ValidationError(
                        _("A senha não pode conter sequências comuns ou padrões previsíveis."),
                        code='password_common_pattern',
                    )
                )
        
        # Verificar se a senha não é muito similar ao nome de usuário
        if user and user.username:
            if password.lower() in user.username.lower() or user.username.lower() in password.lower():
                errors.append(
                    ValidationError(
                        _("A senha não pode ser muito similar ao nome de usuário."),
                        code='password_too_similar',
                    )
                )
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        help_texts = [f"Pelo menos {self.min_length} caracteres"]
        
        if self.require_uppercase:
            help_texts.append("pelo menos uma letra maiúscula")
        if self.require_lowercase:
            help_texts.append("pelo menos uma letra minúscula")
        if self.require_digits:
            help_texts.append("pelo menos um número")
        if self.require_special_chars:
            help_texts.append("pelo menos um caractere especial")
        
        return "A senha deve conter: " + ", ".join(help_texts) + "."


class PasswordHistoryValidator:
    """
    Validador para verificar se a senha não foi usada recentemente
    """
    
    def __init__(self, history_count=5):
        self.history_count = history_count
    
    def validate(self, password, user=None):
        if not user or not user.pk:
            return
        
        # Aqui você implementaria a lógica para verificar o histórico de senhas
        # Por simplicidade, vamos apenas validar que a senha não é igual à atual
        if user.check_password(password):
            raise ValidationError(
                _("A senha deve ser diferente da senha atual."),
                code='password_same_as_current',
            )
    
    def get_help_text(self):
        return f"A senha deve ser diferente das últimas {self.history_count} senhas utilizadas."
