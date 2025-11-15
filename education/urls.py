from django.urls import path
from . import views

urlpatterns = [
    # exemplo: rota para listar publicações educacionais
    path('publications', views.list_publications, name='list_publications'),
    path('publications/create', views.create_publication, name='create_publication'),
    path('publications/<int:id>/edit', views.edit_publication, name='edit_publication'),
    path('publications/<int:id>/delete', views.delete_publication, name='delete_publication'),
    path('publications/filter', views.filter_publications, name='filter_publications'),
    path('publications/filter_by_select2/json', views.filter_publications_by_select2, name='filter_publications_by_select2')
]