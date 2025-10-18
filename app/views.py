from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from app.models import Produto

def lista_produtos(request):
    produtos = Produto.objects.order_by('-criado_em')
    contexto = {'produtos': produtos}
    return render(request, 'lista_produtos.html', contexto)

@require_http_methods(['GET', 'POST'])
def novo_produto(request):
    if request.method == 'GET':
        return render(request, 'produto_form.html')

    nome = request.POST.get('nome')
    preco = request.POST.get('preco')

    if nome and preco:
        Produto.objects.create(nome=nome, preco=preco)
        return redirect('lista_produtos')

    contexto = {'erro': 'Preencha nome e preço corretamente.'}
    return render(request, 'produto_form.html', contexto)

@require_http_methods(['GET', 'POST'])
def atualizar_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return redirect('lista_produtos')

    if request.method == 'GET':
        contexto = {'produto': produto}
        return render(request, 'produto_form.html', contexto)

    nome = request.POST.get('nome')
    preco = request.POST.get('preco')

    if nome and preco:
        try:
            produto.nome = nome
            produto.preco = preco
            produto.save()
            return redirect('lista_produtos')
        except Produto.DoesNotExist:
            contexto = {
                'produto': produto,
                'erro': 'Ocorreu um erro ao salvar. Tente novamente.'
            }
            return render(request, 'produto_form.html', contexto)

    contexto = {
        'produto': produto,
        'erro': 'Preencha nome e preço corretamente.'
    }
    return render(request, 'produto_form.html', contexto)