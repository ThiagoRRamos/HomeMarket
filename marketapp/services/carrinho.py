'''
Created on Apr 5, 2013

@author: thiagorramos
'''
from marketapp.models import CarrinhoCompras, ProdutoCarrinho


class CarrinhoComOutroSupermercado(Exception):
    pass


def limpar_carrinho(usuario):
    CarrinhoCompras.objects.filter(usuario=usuario).delete()


def get_carrinho_usuario(usuario):
    return CarrinhoCompras.objects.get_or_create(usuario=usuario)[0]


def adicionar_produto(usuario, produto_supermercado, quantidade=1):
    try:
        carrinho = CarrinhoCompras.objects.get(usuario=usuario)
        if carrinho.supermercado is None:
            carrinho.supermercado = produto_supermercado.supermercado
            carrinho.save()
    except CarrinhoCompras.DoesNotExist:
        carrinho = CarrinhoCompras.objects.create(usuario=usuario,
                                       supermercado=produto_supermercado.supermercado)
    try:
        produto_carrinho = ProdutoCarrinho.objects.get(produto=produto_supermercado,
                                                          carrinho=carrinho)
        produto_carrinho.quantidade += quantidade
        produto_carrinho.save()
    except ProdutoCarrinho.DoesNotExist:
        if produto_supermercado.supermercado == carrinho.supermercado:
            return ProdutoCarrinho.objects.create(produto=produto_supermercado,
                                                  carrinho=carrinho,
                                                  quantidade=quantidade)
        else:
            raise CarrinhoComOutroSupermercado
