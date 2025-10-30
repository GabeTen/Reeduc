from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import PublicacaoEducacional  # importa o modelo da app educação
from .forms import PublicacaoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def publicacao_list(request):
    all_publicacoes = PublicacaoEducacional.objects.all().order_by('-data_publicacao')

    # Paginação
    paginator = Paginator(all_publicacoes, 8)  # 10 publicações por página
    page = request.GET.get('page')

    try:
        publicacoes = paginator.page(page)
    except PageNotAnInteger:
        publicacoes = paginator.page(1)
    except EmptyPage:
        publicacoes = paginator.page(paginator.num_pages)

    context = {
        'publicacoes': publicacoes,
    }

    return render(request, 'educacao/publicacoes_list.html', context)


@login_required 
def create_publicacao(request):
    if request.method == 'POST':
        form = PublicacaoForm(request.POST) #popula o formulário com os dados submetidos 
        if form.is_valid():
            publicacao = form.save(commit=False) 
            publicacao.autor = request.user 
            publicacao.save() 
            
            return redirect('publicacoes_list') 
    else:
        form = PublicacaoForm()  #retorna um formulário vazio
    
    return render(request, 'educacao/publicacao_form.html', {'form': form})

@login_required
def edit_publicacao(request, id):
    publicacao = get_object_or_404(PublicacaoEducacional, id=id)

    # Autor ou superusuário pode editar
    if publicacao.autor != request.user and not request.user.is_superuser:
        return redirect('publicacoes_list')

    if request.method == 'POST':
        form = PublicacaoForm(request.POST, instance=publicacao)
        if form.is_valid():
            form.save()
            return redirect('publicacoes_list')
    else:
        form = PublicacaoForm(instance=publicacao)
    
    return render(request, 'educacao/publicacao_form.html', {
        'form': form,
        'editar': True
    })

@login_required 
def filter_publicacoes(request):
    title = request.GET.get('title', '')
    description = request.GET.get('description', '')

    publicacoes_list = PublicacaoEducacional.objects.all().order_by('-data_publicacao')

    if title:
        publicacoes_list = publicacoes_list.filter(titulo__icontains=title)
    if description:
        publicacoes_list = publicacoes_list.filter(descricao__icontains=description)

    # --- Re-apply pagination to the filtered results ---
    paginator = Paginator(publicacoes_list, 8)  # 8 per page, just like your main view
    page = request.GET.get('page')

    try:
        publicacoes = paginator.page(page)
    except PageNotAnInteger:
        publicacoes = paginator.page(1)
    except EmptyPage:
        publicacoes = paginator.page(paginator.num_pages)

    context = {
        'publicacoes': publicacoes,
    }

    # 🔹 Retorna O NOVO PARTIAL que contém os cards E a paginação
    return render(request, 'educacao/partials/publicacoes_partial.html', context)



def delete_publicacao(request, id):
    publicacao = get_object_or_404(PublicacaoEducacional, id=id)

    # Verifica permissão
    if request.user != publicacao.autor and not request.user.is_superuser:
        return JsonResponse({'error': 'Sem permissão para excluir.'}, status=403)

    publicacao.delete()
    return JsonResponse({'message': 'Publicação excluída com sucesso!', 'id': id})