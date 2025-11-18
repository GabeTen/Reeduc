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
            return JsonResponse({'success': True, 'redirect_url': '/users/page/'})
        else:
            errors = get_form_errors_as_json(form)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return render(request, 'core/register.html', {'form': UserCreationForm()})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
def edit_data_user(request, id):
    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado.'}, status=404)


    # -----------------------------
    # 1 - Captura segura dos dados
    # -----------------------------
    username    = request.POST.get("username")
    email       = request.POST.get("email")
    first_name  = request.POST.get("firstname")
    last_name   = request.POST.get("lastname")
    password    = request.POST.get("password")
    role        = request.POST.get("role")
    
    def get_bool(name):
        val = request.POST.get(name)
        if val is None:
            return None
        return str(val).lower() in ["true", "1", "on", "yes"]

    is_superuser = get_bool("is_superuser")
    is_staff     = get_bool("is_staff")
    is_active    = get_bool("is_active")


    # -----------------------------
    # 2 - Campos obrigatórios
    # -----------------------------
    if username is None or username.strip() == "":
        return JsonResponse({'success': False, 'error': 'O nome de usuário é obrigatório.'}, status=400)


    # -----------------------------
    # 3 - Configura valores limpos
    # -----------------------------
    clean = {
        "username": username.strip(),
        "email": email.strip() if email else None,
        "first_name": first_name.strip() if first_name else None,
        "last_name": last_name.strip() if last_name else None,
        "role": role.strip().lower() if role else None,
    }


    # -----------------------------
    # 4 - Verifica duplicidade username
    # -----------------------------
    if clean["username"] != user.username:
        if User.objects.filter(username=clean["username"]).exclude(id=user.id).exists():
            return JsonResponse({
                'success': False,
                'message': "Já existe um usuário com esse username."
            }, status=409)


    # -----------------------------
    # 5 - Detecta mudanças reais
    # -----------------------------
    changes = {}

    def check_change(field, new_value):
        old_value = getattr(user, field)
        if new_value is not None and new_value != old_value:
            changes[field] = {"old": old_value, "new": new_value}
            setattr(user, field, new_value)

    # Campos simples
    check_change("username", clean["username"])
    check_change("email", clean["email"])
    check_change("first_name", clean["first_name"])
    check_change("last_name", clean["last_name"])

    # Booleanos
    if is_superuser is not None and is_superuser != user.is_superuser:
        changes["is_superuser"] = {"old": user.is_superuser, "new": is_superuser}
        user.is_superuser = is_superuser

    if is_staff is not None and is_staff != user.is_staff:
        changes["is_staff"] = {"old": user.is_staff, "new": is_staff}
        user.is_staff = is_staff

    if is_active is not None and is_active != user.is_active:
        changes["is_active"] = {"old": user.is_active, "new": is_active}
        user.is_active = is_active


    senha_alterada = False

    # -----------------------------
    # 6 - Senha (tratamento correto)
    # -----------------------------
    if password:
        if not user.check_password(password):   # evita marcar mudança se é a mesma senha
            changes["password"] = {"old": "********", "new": "********"}
            user.set_password(password)
            senha_alterada = True


    # -----------------------------
    # 7 - Role
    # -----------------------------
    current_roles = get_user_roles(user)
    current_role = current_roles[0].role_name if current_roles else None

    if clean["role"] and clean["role"] != current_role:

        changes["role"] = {"old": current_role, "new": clean["role"]}

        # Remove todas as roles anteriores
        for r in ['aluno', 'professor', 'admin']:
            remove_role(user, r)

        assign_role(user, clean["role"])


    # -----------------------------
    # 8 - Nada mudou
    # -----------------------------
    if not changes:
        return JsonResponse({
            "success": False,
            "changed": False,
            "message": "Nenhuma modificação foi realizada."
        })


    # -----------------------------
    # 9 - Salva usuário
    # -----------------------------
    user.save()


    # -----------------------------
    # 10 - Retorno final
    # -----------------------------
    return JsonResponse({
        'success': True,
        'message': "Dados atualizados com sucesso.",
        "changed": True,
        "changes": changes
    })


def get_user_data(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não encontrado.'}, status=404)

    roles = get_user_roles(user)
    role_name = roles[0].role_name if roles else "aluno"

    return JsonResponse({
        "success": True,
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "role": role_name
    })


def delete_user(request, id):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Método não permitido."},
            status=405
        )

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Usuário não encontrado."},
            status=404
        )

    # Impede deletar superuser via painel (opcional)
    if user.is_superuser:
        return JsonResponse(
            {"success": False, "error": "Não é possível excluir um super usuário."},
            status=403
        )

    user.delete()

    return JsonResponse(
        {"success": True, "message": "Usuário excluído com sucesso."},
        status=200
    )