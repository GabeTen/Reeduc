from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from educacao.models import PublicacaoEducacional
from .models import Course
from django.contrib.auth.decorators import login_required
from .forms import CursoForm
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'cursos/course_list.html', {'courses': courses})

@login_required
def course_publications(request, id):
    course = get_object_or_404(Course, id=id)
    publications = course.publicacoes.all()

    return render(request, 'cursos/course_detail.html', {
        'course': course,
        'publications': publications,
    })



@login_required
def filter_cursos(request):
    title = request.GET.get('title', '')
    description = request.GET.get('description', '')
    status = request.GET.get('status', '')

    courses = Course.objects.all()

    if title:
        courses = courses.filter(title__icontains=title)
    if description:
        courses = courses.filter(description__icontains=description)
    if status and status != 'Selecione o status.':
        courses = courses.filter(status=status)

    # 🔹 Retorna apenas o HTML dos cards (partial)
    return render(request, 'cursos/partials/cursos_cards.html', {'courses': courses})


@login_required
def create_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.autor = request.user
            curso.save()

            # ✅ Atualiza as publicações selecionadas
            publicacoes = form.cleaned_data.get('publicacoes')
            if publicacoes:
                publicacoes.update(curso=curso)  # vincula todas ao novo curso

            return redirect('course_list')
    else:
        form = CursoForm()

    return render(request, 'cursos/course_form.html', {'form': form})
