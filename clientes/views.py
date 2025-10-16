from django.shortcuts import render
from clientes.models import Cliente

def lista_clientes(request):
    filtro = request.GET.get('q', '').strip()
    clientes = Cliente.objects.select_related('produto_favorito').order_by('-criado_em')

    if filtro:
        clientes = clientes.filter(nome__icontains=filtro)

    contexto = {
        'clientes': clientes,
        'q': filtro,
    }

    return render(request, 'lista_clientes.html', contexto)