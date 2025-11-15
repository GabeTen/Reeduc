from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_courses, name='list_courses'),
    path('create', views.create_course, name='create_course'),
    path('<int:id>/edit', views.edit_course, name='edit_course'),
    path('<int:id>/delete', views.delete_course, name='delete_course'),
    path('<int:id>', views.course_publications, name='course_publications'),
    path('filter', views.filter_courses, name='filter_courses'),
    path('enrolled', views.enrolled, name='enrolled'),
    path('<int:id>/relationships', views.get_relationships_course, name='get_relationships_course'),
]

