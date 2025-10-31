from django.urls import path
from . import views

urlpatterns = [
    # exemplo: rota para listar publicações educacionais
    path('publicacoes/', views.publicacao_list, name='publicacoes_list'),
    path('publicacoes/create/', views.create_publicacao, name='create_publicacao'),
    path('publicacoes/<int:id>/edit/', views.edit_publicacao, name='edit_publicacao'),
    path('publicacoes/<int:id>/delete/', views.delete_publicacao, name='delete_publicacao'),
    path('publicacoes/filter/', views.filter_publicacoes, name='filter_publicacoes'),
    path('publicacoes/json/', views.listar_publicacoes, name='listar_publicacoes')
]