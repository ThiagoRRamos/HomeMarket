from django.shortcuts import render, get_object_or_404, redirect
from marketapp.models import Supermercado, ProdutoSupermercado
from django.http.response import Http404
import marketapp.services.carrinho as carrinho_service
from marketapp.utils.autorizacao import apenas_cliente
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


@apenas_cliente()
def ver_produtos_supermercado(request, nome):
    try:
        supermercado = Supermercado.objects.get(nome_url=nome)
    except Supermercado.DoesNotExist:
        raise Http404
    produtos = ProdutoSupermercado.objects.filter(supermercado=supermercado)
    return render(request,
                  'ver_produtos_supermercado.html',
                  {'produtos': produtos,
                   'supermercado': supermercado})


@apenas_cliente()
def adicionar_produto_carrinho(request, produto_id):
    produto = get_object_or_404(ProdutoSupermercado, id=produto_id)
    carrinho_service.adicionar_produto(request, produto)
    return redirect('/meu-carrinho')


@login_required
def ver_carrinho(request):
    carrinho = carrinho_service.get_carrinho_usuario(request.user)
    return render(request,
                  'carrinho.html',
                  {'carrinho': carrinho})
