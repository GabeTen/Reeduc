from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from cursos.models import Course
from educacao.models import PublicacaoEducacional, User
from reeduc.utils import get_form_errors_as_json


def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

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

def logout_view(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect_url': '/'})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@login_required
def filter_students_by_select2(request):
    
    termoDeBusca = request.GET.get('q', '')

     # Filtra conforme necessário
    studentsQuerySet = User.objects.filter(username__icontains=termoDeBusca)

    data = [
        {'id': s.id, 'text': s.username}
        for s in studentsQuerySet
    ]
    return JsonResponse({'results': data})