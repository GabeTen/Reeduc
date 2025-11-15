# Create your models here.
import re
from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Course

User = get_user_model()

# null=False,     # ← obrigatório no banco
# blank=False     # ← obrigatório nos formulários

class EducationalPublication(models.Model):
    title = models.CharField(
        verbose_name='Título',
        max_length=50, 
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name='Descrição',
        max_length=200, 
        null=False,
        blank=False
    )
    link = models.URLField(
        verbose_name='Link',
        max_length=300,
        null=False, 
        blank=False
    )
    embed_link = models.URLField(
        verbose_name='Embed Link',
        max_length=300, 
        null=True,
        blank=True
    )
    publication_date = models.DateTimeField(
        verbose_name='Data de Publicação da Publicação Educacional',
        null=False,
        blank=False,
        auto_now_add=True
    )

    # 🔗 Relacionamento com o curso (1:N)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='publications',
        null=True,
        blank=True
    )

    # 🔗 Relacionamento com o usuário (1:N)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='publications',
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.title} ({self.author.username})"
    
    def save(self, *args, **kwargs):

        # 👉 Atualizar embed_link SOMENTE SE o link mudou
        if self.pk:
            old = EducationalPublication.objects.get(pk=self.pk)

            if old.link != self.link:
                self.embed_link = self._extract_dailymotion_embed(self.link)
        else:
            # Primeiro salvamento
            self.embed_link = self._extract_dailymotion_embed(self.link)

        super().save(*args, **kwargs)

    def _extract_dailymotion_embed(self, url):
        """
        Extrai o ID do vídeo de qualquer tipo de link do Dailymotion.
        """
        # Formato normal: dailymotion.com/video/{id}
        match = re.search(r"dailymotion\.com\/video\/([^_?\/]+)", url)
        if match:
            video_id = match.group(1)
            return f"https://www.dailymotion.com/embed/video/{video_id}"

        # Formato encurtado: dai.ly/{id}
        match = re.search(r"dai\.ly\/([^_?\/]+)", url)
        if match:
            video_id = match.group(1)
            return f"https://www.dailymotion.com/embed/video/{video_id}"

        return None