from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PublicacaoEducacional(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    # 🔗 Relacionamento com o usuário (1:N)
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publicacoes'
    )

    def __str__(self):
        return f"{self.titulo} ({self.autor.username})"
