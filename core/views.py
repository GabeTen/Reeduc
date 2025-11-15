from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from courses.models import Course
from education.models import EducationalPublication, User
from reeduc.utils import get_form_errors_as_json
from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import assign_role

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            assign_role(user, 'aluno')
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
        else:
            errors = get_form_errors_as_json(form)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return render(request, 'core/register.html', {'form': UserCreationForm()})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
        else:
            errors = get_form_errors_as_json(form)
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    return render(request, 'core/login.html', {'form': AuthenticationForm()})

@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect_url': '/'})


@has_role_decorator('professor')
@login_required
def filter_students_by_select2(request):
    
    q = request.GET.get('q', '')

     # Filtra conforme necessário
    studentsQuerySet = User.objects.filter(username__icontains=q)

    data = [
        {'id': s.id, 'text': s.username}
        for s in studentsQuerySet
    ]
    return JsonResponse({'results': data})


@login_required
def dashboard(request):

    user_logged = request.user
    total_courses = Course.objects.filter(author = user_logged).count()
    total_publications = EducationalPublication.objects.filter(author = user_logged).count()
    context = {'total_courses': total_courses, 'total_publications': total_publications}

    return render(request, 'core/dashboard.html', context)

def erro_403(request, exception=None):
    """Página exibida quando o usuário não tem permissão de acesso."""
    return render(request, '403.html', status=403)