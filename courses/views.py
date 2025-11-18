from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

from education.models import EducationalPublication, User
from reeduc.field_translations import translate_form_errors
from reeduc.utils import get_form_errors_as_json
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
from django.shortcuts import get_object_or_404, render, redirect
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count



@login_required
@has_role_decorator('professor')
def list_courses(request):
    all_courses = Course.objects.annotate(total_enrolled=Count('students'))


    # Paginação
    paginator = Paginator(all_courses, 8)  # 10 publicações por página
    page = request.GET.get('page')

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {
        'courses': courses,
    }

    return render(request, 'courses/course_list.html', context)

@login_required
def course_publications(request, id):
    course = get_object_or_404(Course, id=id)
    publications = course.publicacoes.all()

    return render(request, 'courses/course_publications.html', {
        'course': course,
        'publications': publications,
    })



@login_required
@has_role_decorator('professor')
def filter_courses(request):
    title = request.GET.get('title', '')
    description = request.GET.get('description', '')
    status = request.GET.get('status', '')

    courses_list = Course.objects.all().order_by('-publication_date')

    if title:
        courses_list = courses_list.filter(title__icontains=title)
    if description:
        courses_list = courses_list.filter(description__icontains=description)
    if status and status != 'Selecione o status.':
        courses_list = courses_list.filter(status=status)

    # --- Re-apply pagination to the filtered results ---
    paginator = Paginator(courses_list, 8)  # 8 per page, just like your main view
    page = request.GET.get('page')

    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {
        'courses': courses,
    }

    # 🔹 Retorna apenas o HTML dos cards (partial)
    return render(request, 'courses/partials/courses_partial.html', context)

@login_required
@has_role_decorator('professor')
def create_course(request):
    publicationsQuerySet = EducationalPublication.objects.filter(course__isnull=True)
    studentsQuerySet = User.objects.all()


    if request.method == 'POST':

        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()

            publications_ids = request.POST.getlist('publications')  # ← lista de valores
            students_ids = request.POST.getlist('students')  # ← lista de valores


            #Associando o curso às Publicacoes Educacionais
            for pub_id in publications_ids:
                pub = publicationsQuerySet.get(id=pub_id)
                pub.course = course
                pub.save()

            #Associando o curso aos usuários/estudantes
            for student_id in students_ids:
                stud = studentsQuerySet.get(id=student_id)
                Enrollment.objects.create(course=course, user=stud)


            return JsonResponse({
                'success': True,
                'mensagem': 'Curso criado com sucesso!',
                'redirect_url': '/course_list'
            })

        else:
            errors = get_form_errors_as_json(form)
            errors_translated = translate_form_errors(errors)
            return JsonResponse({'success': False, 'errors': errors_translated}, status=400)
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form})


#trabalhando nesse enpoint
@login_required
@has_role_decorator('professor')
def edit_course(request, id):

    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({
                'success': False,
                'message': 'Curso não encontrado !'
            })
    
    # Permissão
    if course.author != request.user and not request.user.is_superuser:
        return JsonResponse({
            'success': False,
            'message': 'Você não tem permissão para editar este curso.',
            'redirect_url': '/course_list'
        }, status=403)
    
    
    if request.method == 'GET':
        # Recupera os objetos relacionados
        related_publications = EducationalPublication.objects.filter(course=course)
        related_students = course.students.all()

        # Passa os valores iniciais para o formulário
        form = CourseForm(
            instance=course,
            initial={
                'publications': related_publications,
                'students': related_students
            }
        )

        return render(
            request,
            'courses/course_form.html',
            {
                'form': form,
                'edit': True,
                'course': course
            }
        )

    elif request.method == 'POST':
        form = CourseForm(request.POST, instance=course)

        # Dados enviados pelo formulário
        publications_ids = [int(x) for x in request.POST.getlist('publications')]
        students_ids = [int(x) for x in request.POST.getlist('students')]

        # Dados atuais no banco
        current_publications = list(
            EducationalPublication.objects.filter(course=course).values_list('id', flat=True)
        )
        current_students = list(
            course.students.values_list('id', flat=True)
        )

        # 🔍 Verificar se houve mudança nas publicações
        edited_publications = set(publications_ids) != set(current_publications)

        # 🔍 Verificar se houve mudança nos estudantes
        students_changed = set(students_ids) != set(current_students)

        # 🔍 Verificar se o form foi alterado (campos simples)
        if not form.has_changed() and not edited_publications and not students_changed:
            return JsonResponse({
                'success': False,
                'message': 'Nenhuma alteração detectada — o curso permanece igual.'
            })

        if form.is_valid():
            course = form.save(commit=False)
            course.save()

            publications_ids = request.POST.getlist('publications')  # ← lista de valores
            students_ids = request.POST.getlist('students')  # ← lista de valores

            # Atualiza publicações associadas
            EducationalPublication.objects.filter(course=course).update(course=None)
            EducationalPublication.objects.filter(id__in=publications_ids).update(course=course)

            # Atualiza estudantes (tabela intermediária)
            course.students.clear()
            for student_id in students_ids:
                stud = User.objects.get(id=student_id)
                course.students.add(stud)

            return JsonResponse({
                'success': True,
                'message': 'Curso atualizada com sucesso!',
                'redirect_url': '/course_list'
            })
        else:
            errors = get_form_errors_as_json(form)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
    else:
        form = CourseForm(instance=course)
    
    return render(
        request,
        'courses/course_form.html', 
        {
            'form': form,
            'edit': True,
            'course': course
        }
    )


@has_role_decorator('professor')
@login_required
def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Curso não encontrado.'}, status=404)

    # Verifica permissão
    if request.user != course.author and not request.user.is_superuser:
        return JsonResponse({'error': 'Sem permissão para excluir.'}, status=403)

    course.delete()
    return JsonResponse({'message': 'Curso excluída com sucesso!', 'id': id})



@login_required
def enrolled(request):
    """
    Exibe os cursos em que o aluno logado está matriculado.
    """
    user = request.user
    courses = Course.objects.filter(author=user)

    context = {
        'courses': courses
    }

    return render(request, 'courses/enrolled.html', context)

@login_required
@has_role_decorator('professor')
def get_relationships_course(request, id):
    
    course = Course.objects.get(id=id)
  
    students = course.students.all()
    publications = EducationalPublication.objects.filter(course=course)
    
    data = {
        'publications': [{'id': p.id, 'text': p.title} for p in publications],
        'students': [{'id': e.id, 'text': e.username} for e in students],
    }
    return JsonResponse(data)
