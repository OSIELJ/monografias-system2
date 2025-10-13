from django.contrib import admin
from .models import Aluno, Orientador, Coorientador, Monografia, Banca

admin.site.register(Aluno)
admin.site.register(Orientador)
admin.site.register(Coorientador)
admin.site.register(Monografia)
admin.site.register(Banca)