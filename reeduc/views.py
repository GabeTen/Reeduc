from django.shortcuts import render

def erro_403(request, exception=None):
    """Página exibida quando o usuário não tem permissão de acesso."""
    return render(request, '403.html', status=403)