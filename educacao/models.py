from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PublicacaoEducacional(models.Model):
    titulo = models.CharField(max_length=200, null=False)
    descricao = models.TextField(null=False)
    link = models.URLField(max_length=300, null=True, blank=True)
    embed_link = models.URLField(max_length=300, null=True, blank=True, editable=False)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    # 🔗 Relacionamento com o usuário (1:N)
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publicacoes'
    )

    def __str__(self):
        return f"{self.titulo} ({self.autor.username})"
    
    def save(self, *args, **kwargs):
        if self.link:
            self.embed_link = self.link.replace('watch?v=', 'embed/')
        super().save(*args, **kwargs)
