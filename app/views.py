from django.shortcuts import render
from app.models import Produto

def lista_produtos(request):
    produtos = Produto.objects.order_by('-criado_em')
    contexto = {'produtos': produtos}
    return render(request, 'lista.html', contexto)
