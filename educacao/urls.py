from django.urls import path
from . import views

urlpatterns = [
    # exemplo: rota para listar publicações educacionais
    path('publicacoes/', views.publicacao_list, name='publicacoes_list'),
    path('create/', views.create_publicacao, name='create_publicacao'),
    path('<int:pk>/edit/', views.edit_publicacao, name='edit_publicacao'),
    path('<int:pk>/delete/', views.delete_publicacao, name='delete_publicacao'),
]