from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403


urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 inclui todas as rotas da app core
    path('', include('core.urls')),

    # 👇 inclui as rotas da app educacao
    path('education/', include('education.urls')),

     # 👇 inclui as rotas da app cursos
    path('courses/', include('courses.urls')),
]

handler403 = 'core.views.erro_403'