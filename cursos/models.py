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

class Activity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'activity')

    def __str__(self):
        return f"{self.user.username} - {self.activity.title} ({'Concluída' if self.completed else 'Pendente'})"
