from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("monografias/", views.monografia_list, name="monografia_list"),
    path("monografias/nova/", views.monografia_create, name="monografia_create"),
    path("monografias/<int:pk>/editar/", views.monografia_edit, name="monografia_edit"),
    path("monografias/<int:pk>/excluir/", views.monografia_delete, name="monografia_delete"),
]
