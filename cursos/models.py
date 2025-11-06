from django.db import models
from django.contrib.auth.models import User

from enum import Enum

class CourseStatus(models.TextChoices):
    ATIVO = 'Ativo', 'Ativo'
    PENDENTE = 'Pendente', 'Pendente'
    INATIVO = 'Inativo', 'Inativo'


class Course(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
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

    # 🔗 Relacionamento com o usuário (N:N)
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='courses'
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"