from django.db import models
from django.contrib.auth.models import User

from enum import Enum

class CourseStatus(models.TextChoices):
    ATIVO = 'Ativo', 'Ativo'
    PENDENTE = 'Pendente', 'Pendente'
    INATIVO = 'Inativo', 'Inativo'


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=CourseStatus.choices,
        default=CourseStatus.PENDENTE
    )

    # 🔗 Relacionamento com o usuário (1:N)
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cursos'
    )

    def __str__(self):
        return self.title

