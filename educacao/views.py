from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PublicacaoEducacional  # importa o modelo da app educação


def publicacoes_list(request):
    # 🔹 Lista simulada de publicações (em memória)
    publicacoes = [
        {
            'titulo': 'A Importância da Educação Digital',
            'descricao': 'Um estudo sobre o impacto das tecnologias na aprendizagem moderna.',
            'autor': 'Eugenio Lima',
            'data_publicacao': '2025-10-20 18:00',
        },
        {
            'titulo': 'Metodologias Ativas na Sala de Aula',
            'descricao': 'Explorando o papel do aluno como protagonista no processo de ensino-aprendizagem.',
            'autor': 'Ana Souza',
            'data_publicacao': '2025-10-18 09:30',
        },
        {
            'titulo': 'Ensino Híbrido e o Futuro da Educação',
            'descricao': 'Como combinar o ensino presencial e remoto de forma eficiente.',
            'autor': 'Carlos Pereira',
            'data_publicacao': '2025-10-15 15:45',
        },
        {
            'titulo': 'A Importância da Educação Digital',
            'descricao': 'Um estudo sobre o impacto das tecnologias na aprendizagem moderna.',
            'autor': 'Eugenio Lima',
            'data_publicacao': '2025-10-20 18:00',
        },
        {
            'titulo': 'Metodologias Ativas na Sala de Aula',
            'descricao': 'Explorando o papel do aluno como protagonista no processo de ensino-aprendizagem.',
            'autor': 'Ana Souza',
            'data_publicacao': '2025-10-18 09:30',
        },
        {
            'titulo': 'Ensino Híbrido e o Futuro da Educação',
            'descricao': 'Como combinar o ensino presencial e remoto de forma eficiente.',
            'autor': 'Carlos Pereira',
            'data_publicacao': '2025-10-15 15:45',
        },
        {
            'titulo': 'A Importância da Educação Digital',
            'descricao': 'Um estudo sobre o impacto das tecnologias na aprendizagem moderna.',
            'autor': 'Eugenio Lima',
            'data_publicacao': '2025-10-20 18:00',
        },
        {
            'titulo': 'Metodologias Ativas na Sala de Aula',
            'descricao': 'Explorando o papel do aluno como protagonista no processo de ensino-aprendizagem Explorando o papel do aluno como protagonista no processo de ensino-aprendizagem.',
            'autor': 'Ana Souza',
            'data_publicacao': '2025-10-18 09:30',
        },
        {
            'titulo': 'Ensino Híbrido e o Futuro da Educação',
            'descricao': 'Como combinar o ensino presencial e remoto de forma eficiente.',
            'autor': 'Carlos Pereira',
            'data_publicacao': '2025-10-15 15:45',
        },
    ]

    # Renderiza o template com a lista em memória
    return render(request, 'educacao/publicacoes_list.html', {'publicacoes': publicacoes})