from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from app.models import Produto
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

@require_http_methods(['GET', 'POST'])
def novo_cliente(request):
    if request.method == 'GET':
        produtos = Produto.objects.order_by("nome")
        return render(request, 'cliente_form.html', {'produtos': produtos})

    nome = request.POST.get('nome').strip()
    email = request.POST.get('email').strip()
    produto_id = request.POST.get('produto_favorito')

    if nome and email:
        produto_favorito = None
        if produto_id:
            try:
                produto_favorito = Produto.objects.get(id=produto_id)
            except Produto.DoesNotExist:
                produto_favorito = None

        Cliente.objects.create(
            nome=nome,
            email=email,
            produto_favorito=produto_favorito
        )
        return redirect('lista_clientes')

    produtos = Produto.objects.order_by("nome")
    contexto = {
        'erro': 'Preencha nome e email corretamente.',
        'produtos': produtos
    }
    return render(request, 'cliente_form.html', contexto)

@require_http_methods(['GET', 'POST'])
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        nome = request.POST.get('nome').strip()
        email = request.POST.get('email').strip()
        produto_id = request.POST.get('produto_favorito', '').strip()

        if not nome or not email:
            produtos = Produto.objects.order_by("nome")
            contexto = {
                'cliente': cliente,
                'produtos': produtos,
                'erro': 'Preencha nome e email corretamente.',
                'nome': nome,
                'email': email,
            }
            return render(request, 'cliente_form.html', contexto)

        cliente.nome = nome
        cliente.email = email

        if produto_id:
            cliente.produto_favorito = get_object_or_404(Produto, id=produto_id)
        else:
            cliente.produto_favorito = None

        cliente.save()
        return redirect('lista_clientes')

    produtos = Produto.objects.order_by("nome")
    contexto = {
        'cliente': cliente,
        'produtos': produtos,
    }

    return render(request, 'cliente_form.html', contexto)