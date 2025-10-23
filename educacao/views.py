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