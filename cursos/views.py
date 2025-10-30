from django.shortcuts import render, get_object_or_404
from .models import Course, Activity, UserActivity
from django.contrib.auth.decorators import login_required
from .forms import CursoForm
from django.shortcuts import get_object_or_404, render, redirect


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'cursos/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    activities = course.activities.all()

    for activity in activities:
        UserActivity.objects.get_or_create(user=request.user, activity=activity)

    return render(request, 'cursos/course_detail.html', {
        'course': course,
        'activities': activities,
    })

@login_required
def pending_activities(request):
    pendentes = UserActivity.objects.filter(user=request.user, completed=False)
    return render(request, 'cursos/pending_activities.html', {'pendentes': pendentes})

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
            curso.save()
            
            return redirect('course_list') 
    else:
        form = CursoForm()
    
    return render(request, 'cursos/course_form.html', {'form': form})