from django.db import models
from django.contrib.auth.models import User

class CourseStatus(models.TextChoices):
    ATIVO = 'Ativo', 'Ativo'
    PENDENTE = 'Pendente', 'Pendente'
    INATIVO = 'Inativo', 'Inativo'

# null=False,     # ← obrigatório no banco
# blank=False     # ← obrigatório nos formulários
class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name='Descrição',
        null=False,
        blank=False
    )
    publication_date = models.DateField(
        verbose_name='Data de publicação',
        auto_now_add=True,
        null=False,
        blank=False
    )
    status = models.CharField(
        verbose_name='Status',
        max_length=20,
        choices=CourseStatus.choices,
        default=CourseStatus.PENDENTE,
        null=False,
        blank=False
    )

    # 🔗 Relacionamento com o usuário (1:N)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_authored',
        null=False,
        blank=False
    )

    # 🔗 Relacionamento com o usuário (N:N)
    students = models.ManyToManyField(
        User,
        through='enrollment',
        related_name='courses_enrolled'
    )

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(
        verbose_name='Data da Matrícula do curso',
        auto_now_add=True,    
        null=False,
        blank=False    
    )

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"