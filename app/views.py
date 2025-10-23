from io import BytesIO

from django.db.models import Count
from django.http.multipartparser import MultiPartParser
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Produto
from clientes.models import Cliente


def dashboard(request):
    # Totais simples
    total_produtos = Produto.objects.count()
    total_clientes = Cliente.objects.count()

    # Quantos produtos possuem pelo menos um cliente que os favoritou
    produtos_favoritados_distintos = (
        Cliente.objects
        .filter(produto_favorito__isnull=False)
        .values('produto_favorito')
        .distinct()
        .count()
    )

    # TOP 5 produtos mais favoritados
    # Agrupa clientes por produto favorito, ignora nulos e ordena pela pelo total
    top_favoritos = (
        Cliente.objects
        .filter(produto_favorito__isnull=False)
        .values('produto_favorito', 'produto_favorito__nome')
        .annotate(total=Count('id'))
        .order_by('-total', 'produto_favorito__nome')[:5]
    )

    contexto = {
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'produtos_com_favorito': produtos_favoritados_distintos,
        'top_favoritos': top_favoritos,
    }

    return render(request, 'dashboard.html', contexto)

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

@require_http_methods(['GET', 'PUT'])
def atualizar_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return redirect('lista_produtos')

    if request.method == 'GET':
        contexto = {'produto': produto}
        return render(request, 'produto_form.html', contexto)

    # Monta o parser para interpretar o corpo da requisição PUT
    stream = BytesIO(request.body)
    parser = MultiPartParser(request.META, stream, request.upload_handlers, request.encoding)

    # data é um QueryDict com os campos do formulário
    # files são os arquivos enviados (se houver)
    data, files = parser.parse()

    nome = data.get('nome', '').strip()
    preco = data.get('preco', '').replace(',', '.').strip()

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

@require_http_methods(['DELETE'])
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    contexto = { 'mensagem': 'Excluído com sucesso.' }
    return render(request, 'lista_produtos.html', contexto)