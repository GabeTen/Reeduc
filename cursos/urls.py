from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('novo/', views.create_curso, name='create_curso'),
    path('<int:id>/', views.course_publications, name='course_publications'),
    path('filter/', views.filter_cursos, name='filter_cursos'),
]

