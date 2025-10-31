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
        fields = ['title', 'description', 'status', 'publicacoes']  # ✅ adicionamos publicacoes
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'select2'}),
        }