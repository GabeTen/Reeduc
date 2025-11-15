from django import forms
from education.models import EducationalPublication
from django.contrib.auth.models import User
from .models import Course
from django.db.models import Q


class CourseForm(forms.ModelForm):

    def clean_title(self):
        return self.cleaned_data['title'].strip()
    def clean_description(self):
        return self.cleaned_data['description'].strip()

    # 🔹 Campos extras (não pertencem diretamente ao modelo)
    publications = forms.ModelMultipleChoiceField(
        queryset=EducationalPublication.objects.filter(course__isnull=True).order_by('-publication_date'),
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2 id_publications',
            'data-placeholder': 'Selecione publicações educacionais',
        }),
        label='Publicações Educacionais'
    )

    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2 id_students',
            'data-placeholder': 'Selecione os estudantes',
        }),
        label='Estudantes'
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'status']  # apenas os campos reais do modelo
        labels = {
            'title': 'Título do Curso',
            'description': 'Descrição',
            'status': 'Status',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do curso',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o curso'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Ajusta os querysets dinamicamente conforme o contexto:
        - Se estiver criando um curso: apenas publicações sem curso.
        - Se estiver editando: inclui as publicações já associadas a este curso.
        """
        super().__init__(*args, **kwargs)
        course = kwargs.get('instance', None)

        if course:
            self.fields['publications'].queryset = EducationalPublication.objects.filter(
                Q(course__isnull=True) | Q(course=course)
            ).order_by('-publication_date')
