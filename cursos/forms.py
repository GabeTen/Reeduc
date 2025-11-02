from django import forms

from educacao.models import PublicacaoEducacional
from .models import Course

class CursoForm(forms.ModelForm):
    publicacoes = forms.ModelMultipleChoiceField(
        queryset=PublicacaoEducacional.objects.filter(curso__isnull=True).order_by('-data_publicacao'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2'}),
        required=False,
        label="Publicações Educacionais"
    )

    class Meta:
        model = Course
        fields = ['titulo', 'descricao', 'status', 'publicacoes']  # ✅ adicionamos publicacoes
  