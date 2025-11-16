from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/filter_by_select2/json/', views.filter_students_by_select2, name='filter_students_by_select2'),
    path('users/data/', views.users_data, name="users_data"),
    path('users/page/', views.users_page, name="users_page"),
    path('users/<int:id>/edit/role/', views.edit_role_user, name="edit_role_user")
]
