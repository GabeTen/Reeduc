from django import forms
from .models import PublicacaoEducacional

class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = PublicacaoEducacional
        fields = ['titulo', 'descricao', 'link']