#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monografias.settings')
    django.setup()
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Criar superusuário programaticamente
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@monografias.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            tipo_usuario='ADMIN'
        )
        print("Superusuario criado com sucesso!")
        print("Usuario: admin")
        print("Senha: admin123")
    else:
        print("Superusuario ja existe!")
