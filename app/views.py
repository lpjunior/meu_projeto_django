from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from app.models import Produto

def lista_produtos(request):
    produtos = Produto.objects.order_by('-criado_em')
    contexto = {'produtos': produtos}
    return render(request, 'lista_produtos.html', contexto)

@require_http_methods(['GET'])
def formulario_produto(request):
    return render(request, 'novo_produto.html')

@require_http_methods(['POST'])
def cadastrar_produto(request):
    nome = request.POST.get('nome')
    preco = request.POST.get('preco')

    if nome and preco:
        Produto.objects.create(nome=nome, preco=preco)
        return redirect('lista_produtos')

    contexto = {'erro': 'Preencha nome e preço corretamente.'}
    return render(request, 'novo_produto.html', contexto)