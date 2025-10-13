from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import os


def validate_pdf_file(value):
    """
    Validador para garantir que o arquivo é um PDF válido
    """
    # Verificar extensão
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError(_('Apenas arquivos PDF são permitidos.'))
    
    # Verificar tamanho (máximo 10MB)
    if value.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError(_('O arquivo deve ter no máximo 10MB.'))
    
    # Verificar se o arquivo não está vazio
    if value.size == 0:
        raise ValidationError(_('O arquivo não pode estar vazio.'))
    
    # Verificação básica do header PDF
    value.seek(0)
    header = value.read(4)
    if not header.startswith(b'%PDF'):
        raise ValidationError(_('O arquivo deve ser um PDF válido.'))


def validate_file_size(value):
    """
    Validador para verificar o tamanho do arquivo
    """
    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError(_('O arquivo deve ter no máximo 10MB.'))


def validate_file_extension(value):
    """
    Validador para verificar a extensão do arquivo
    """
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = os.path.splitext(value.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise ValidationError(
            _('Apenas arquivos com extensões %(extensions)s são permitidos.'),
            params={'extensions': ', '.join(allowed_extensions)}
        )
