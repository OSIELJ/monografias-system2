from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import models
from .models import Monografia
from .forms import MonografiaForm


# === Dashboard com filtragem por tipo de usuário ===
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

    return render(request, "core/dashboard.html", {"monografias": monografias})


# === Listagem ===
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

    return render(request, "core/monografia_list.html", {"monografias": monografias})


# === Criação ===
@login_required
def monografia_create(request):
    user = request.user

    # Apenas professores e administradores podem criar
    if not user.is_superuser and getattr(user, "tipo_usuario", None) != "PROF":
        return HttpResponseForbidden("Apenas professores e administradores podem cadastrar monografias.")

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
def monografia_edit(request, pk):
    user = request.user
    monografia = get_object_or_404(Monografia, pk=pk)

    # Professores podem editar apenas suas orientações; alunos e outros não
    if not user.is_superuser and getattr(user, "tipo_usuario", None) != "PROF":
        return HttpResponseForbidden("Apenas professores e administradores podem editar monografias.")

    # Professores só podem editar suas próprias monografias
    if getattr(user, "tipo_usuario", None) == "PROF" and not (
        monografia.orientador and monografia.orientador.usuario.email == user.email
    ):
        return HttpResponseForbidden("Você só pode editar monografias que orienta.")

    form = MonografiaForm(request.POST or None, request.FILES or None, instance=monografia)
    if form.is_valid():
        form.save()
        messages.success(request, "Monografia atualizada com sucesso!")
        return redirect("monografia_list")

    return render(request, "core/monografia_form.html", {"form": form, "monografia": monografia})


# === Exclusão ===
@login_required
def monografia_delete(request, pk):
    user = request.user
    monografia = get_object_or_404(Monografia, pk=pk)

    # Somente administradores podem excluir
    if not user.is_superuser:
        return HttpResponseForbidden("Apenas administradores podem excluir monografias.")

    if request.method == "POST":
        monografia.delete()
        messages.success(request, "Monografia excluída com sucesso!")
        return redirect("monografia_list")

    return render(request, "core/monografia_confirm_delete.html", {"monografia": monografia})
