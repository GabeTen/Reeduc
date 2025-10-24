from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PublicacaoEducacional  # importa o modelo da app educação
from .forms import PublicacaoForm

def publicacao_list(request):
    all_publicacoes = PublicacaoEducacional.objects.all().order_by('-data_publicacao')

    context = {
        'publicacoes': all_publicacoes
    }
    
    return render(request, 'educacao/publicacoes_list.html', context)

@login_required 
def create_publicacao(request):
    if request.method == 'POST':
        form = PublicacaoForm(request.POST) 
        if form.is_valid():
            publicacao = form.save(commit=False) 
            publicacao.autor = request.user  
            publicacao.save() 
            
            return redirect('publicacoes_list') 
    else:
        form = PublicacaoForm() 
    
    return render(request, 'educacao/publicacao_form.html', {'form': form})

@login_required
def edit_publicacao(request, pk):
    publicacao = PublicacaoEducacional.objects.get(pk=pk)

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
def delete_publicacao(request, pk):
    publicacao = PublicacaoEducacional.objects.get(pk=pk)

    # Autor ou superusuário pode excluir
    if publicacao.autor != request.user and not request.user.is_superuser:
        return redirect('publicacoes_list')

    if request.method == 'POST':
        publicacao.delete()
        return redirect('publicacoes_list')

    return render(request, 'educacao/publicacao_confirm_delete.html', {
        'publicacao': publicacao
    })