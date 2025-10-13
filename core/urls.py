from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("monografias/", views.monografia_list, name="monografia_list"),
    path("monografias/nova/", views.monografia_create, name="monografia_create"),
    path("monografias/<int:pk>/", views.monografia_detail, name="monografia_detail"),
    path("monografias/<int:pk>/editar/", views.monografia_edit, name="monografia_edit"),
    path("monografias/<int:pk>/excluir/", views.monografia_delete, name="monografia_delete"),
    # Rota para baixar o PDF binário (o nome 'baixar_pdf' deve corresponder ao template)
    path('monografias/<int:pk>/download/pdf/', views.baixar_pdf, name='baixar_pdf'),
    # Rota para AJAX - obter coorientadores
    path('ajax/get-coorientadores/', views.get_coorientadores, name='get_coorientadores'),
]
