'''
Created on Apr 5, 2013

@author: thiagorramos
'''
from marketapp.models import CarrinhoCompras, ProdutoCarrinho
from marketapp.services.regiao_atendimento import atende


class CarrinhoComOutroSupermercado(Exception):
    pass


class SupermercadoNaoAtendeUsuario(Exception):
    pass


def gerar_lista_de_compras(carrinho, nome=None):
    return carrinho.gerar_lista_compras(nome)


def limpar_carrinho(usuario):
    carrinho = get_carrinho_usuario(usuario)
    carrinho.produtocarrinho_set.all().delete()
    carrinho.delete()


def get_carrinho_usuario(usuario):
    return CarrinhoCompras.objects.get_or_create(usuario=usuario)[0]


def adicionar_produto(usuario, produto_supermercado, quantidade=1):
    try:
        carrinho = CarrinhoCompras.objects.get(usuario=usuario)
        if carrinho.supermercado is None:
            if atende(produto_supermercado.supermercado, usuario):
                carrinho.supermercado = produto_supermercado.supermercado
                carrinho.save()
            else:
                raise SupermercadoNaoAtendeUsuario
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


def carregar_carrinho(usuario, produto_supermercado_map):
    for psm in produto_supermercado_map:
        adicionar_produto(usuario, psm, produto_supermercado_map[psm])