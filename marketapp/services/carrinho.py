'''
Created on Apr 5, 2013

@author: thiagorramos
'''
from marketapp.models import CarrinhoCompras, ProdutoCarrinho


def get_carrinho_usuario(request):
    return CarrinhoCompras.objects.get_or_create(usuario=request.user)[0]


def adicionar_produto(request, produto_supermercado, quantidade=1):
    try:
        carrinho = CarrinhoCompras.objects.get(usuario=request.user)
    except CarrinhoCompras.DoesNotExist:
        carrinho = CarrinhoCompras.objects.create(usuario=request.user,
                                       supermercado=produto_supermercado.supermercado)
    if produto_supermercado.supermercado == carrinho.supermercado:
        return ProdutoCarrinho.objects.create(produto=produto_supermercado,
                                              carrinho=carrinho,
                                              quantidade=quantidade)
