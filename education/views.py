from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from reeduc.field_translations import translate_form_errors
from reeduc.utils import get_form_errors_as_json
from .models import EducationalPublication  # importa o modelo da app educação
from .forms import PublicationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rolepermissions.decorators import has_role_decorator

@login_required
@has_role_decorator('professor')
def list_publications(request):
    all_publications = EducationalPublication.objects.all().order_by('-publication_date')

    # Paginação
    paginator = Paginator(all_publications, 8)  # 10 publicações por página
    page = request.GET.get('page')

    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)

    context = {
        'publications': publications,
    }

    return render(request, 'education/publication_list.html', context)


@login_required 
@has_role_decorator('professor')
def create_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST) #popula o formulário com os dados submetidos 
        if form.is_valid():
            publication = form.save(commit=False) 
            publication.author = request.user 
            publication.save() 
            
            return JsonResponse({
                    'success': True,
                    'message': 'Publicação criada com sucesso!',
                    'redirect_url': '/publication_list'
            })
        
        else:
            errors = get_form_errors_as_json(form)
            errors_translated = translate_form_errors(errors)
            return JsonResponse({
                    'success': False, 
                    'errors': errors_translated
                },status=400)

    else:
        form = PublicationForm()  #retorna um formulário vazio
    
    return render(request, 'education/publication_form.html', {
        'form': form 
    })

@login_required
@has_role_decorator('professor')
def edit_publication(request, id):

    try:
        publication = EducationalPublication.objects.get(id=id)
    except EducationalPublication.DoesNotExist:
        return JsonResponse({
                'success': False,
                'message': 'Publicacao Educacional não encontrada !'
            })

    # Autor ou superusuário pode editar
    if publication.author != request.user and not request.user.is_superuser:
        return JsonResponse({
                'success': False,
                'message': 'Você não tem permissão para editar esta publicacao educacional!',
                'redirect_url': '/publication_list'
            })

    if request.method == 'POST':
        form = PublicationForm(request.POST, instance=publication)

        if not form.has_changed():
            return JsonResponse({
                'success': False,
                'message': 'Nenhuma alteração detectada — a publicacao permanece igual.'
            })

        if form.is_valid():

            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Publicação atualizada com sucesso!',
                'changed_data': form.changed_data,
                'initial': form.initial,
                'redirect_url': '/publication_list'
            })
        else:
            errors = get_form_errors_as_json(form)
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    else:
        form = PublicationForm(instance=publication)
    
    return render(request, 'education/publication_form.html', {
        'form': form,
        'edit': True,
        'publication': publication
    })

@login_required 
def filter_publications(request):
    title = request.GET.get('title', '')
    description = request.GET.get('description', '')

    publications_list = EducationalPublication.objects.all().order_by('-publication_date')

    if title:
        publications_list = publications_list.filter(title__icontains=title)
    if description:
        publications_list = publications_list.filter(description__icontains=description)

    # --- Re-apply pagination to the filtered results ---
    paginator = Paginator(publications_list, 8)  # 8 per page, just like your main view
    page = request.GET.get('page')

    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)

    context = {
        'publications': publications,
    }

    # 🔹 Retorna O NOVO PARTIAL que contém os cards E a paginação
    return render(request, 'education/partials/publications_partial.html', context)


@has_role_decorator('professor')
@login_required
def delete_publication(request, id):
    try:
        publication = EducationalPublication.objects.get(id=id)
    except EducationalPublication.DoesNotExist:
        return JsonResponse({
                    'sucess': False,
                    'message': 'Publicação não encontrado.'
                }
            , status=404)

    # Verifica permissão
    if request.user != publication.author and not request.user.is_superuser:
        return JsonResponse({
                'sucess': False,
                'error': 'Sem permissão para excluir.'
            }, status=403)

    publication.delete()
    return JsonResponse({
                'sucess': True,
                'message': 'Publicação excluída com sucesso!', 
                'id': id
            }, status=200)


@login_required
@has_role_decorator('professor')
def filter_publications_by_select2(request):

    q = request.GET.get('term', '')
    course_id  = request.GET.get('course', 0)

    # Filtra conforme necessário (ex: apenas sem curso ou as já associadas)
    queryset = EducationalPublication.objects.filter(
        Q(course__isnull=True) |  Q(course_id=course_id )
    )
    # Recuperando baseado no termo de busca
    if q:
        queryset = queryset.filter(title__icontains=q)

    data = [
        {'id': p.id, 'text': p.title}
        for p in queryset.order_by('-publication_date')
    ]
    return JsonResponse({'results': data})

