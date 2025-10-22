from django.urls import path
from . import views

urlpatterns = [
    # exemplo: rota para listar publicações educacionais
    path('publicacoes/', views.publicacoes_list, name='publicacoes_list'),
]