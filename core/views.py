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
from django.db.models import Q
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import remove_role

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




@login_required
def users_page(request):
    return render(request, 'core/admin.html')

# @has_role_decorator('admin')
@login_required
def users_data(request):
    # ---- parâmetros enviados pelo DataTable ----
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    search_value = request.GET.get("search[value]", "")
    order_column = request.GET.get("order[0][column]", "0")
    order_dir = request.GET.get("order[0][dir]", "asc")

    # ---- mapear colunas exatamente como no DataTable ----
    columns = [
        "last_login",
        "is_superuser",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    ]

    order_field = columns[int(order_column)]
    if order_dir == "desc":
        order_field = "-" + order_field

    # ---- Query base ----
    queryset = User.objects.all()

    records_total = queryset.count()

    # ---- Filtro global (busca) ----
    if search_value:
        queryset = queryset.filter(
            Q(username__icontains=search_value) |
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(email__icontains=search_value)
        )

    records_filtered = queryset.count()

    # ---- Ordenação ----
    queryset = queryset.order_by(order_field)

    # ---- Paginação ----
    queryset = queryset[start:start + length]

    # ---- Montar os dados para o DataTable ----
    data = []
    for user in queryset:
        roles = get_user_roles(user)
        role_name = roles[0].get_name() if roles else "aluno" 

        data.append({
            "last_login": user.last_login.strftime("%d/%m/%Y %H:%M") if user.last_login else "-",
            "is_superuser": "Sim" if user.is_superuser else "Não",
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_staff": "Sim" if user.is_staff else "Não",
            "is_active": "Ativo" if user.is_active else "Inativo",
            "date_joined": user.date_joined.strftime("%d/%m/%Y %H:%M"),
            "role": role_name,     
            "id": user.id       
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data
    })

@has_role_decorator('admin')
@login_required
def edit_role_user(request, id):
    """
    Edita o papel (role) de um usuário — somente admin pode fazer isso.
    """
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado.'}, status=404)

    # Pega o novo papel enviado pelo frontend
    new_role = request.POST.get("role")

    if not new_role:
        return JsonResponse({'success': False, 'error': 'Nenhum papel informado.'}, status=400)

    # Lista de roles permitidos no sistema
    ROLES_VALIDOS = ['aluno', 'professor', 'admin']

    if new_role not in ROLES_VALIDOS:
        return JsonResponse({'success': False, 'error': 'Papel inválido.'}, status=400)

    # Remove todos os papéis existentes
    for role in ROLES_VALIDOS:
        remove_role(user, role)

    # Atribui o novo papel
    assign_role(user, new_role)

    return JsonResponse({
        'success': True,
        'message': f"Papel do usuário atualizado para: {new_role}"
    })

