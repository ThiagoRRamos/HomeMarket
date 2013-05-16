'''
Created on May 15, 2013

@author: thiagorramos
'''
from marketapp.models import Compra, ProdutoCompra
import marketapp.services.regiao_atendimento as regiao_service


def gerar_compra(consumidor, produtos):
    supermercado = produtos[0].produto.supermercado
    compra = Compra.objects.create(modo_pagamento='nn',
                                   status_pagamento='pn',
                                   consumidor=consumidor,
                                   supermercado=supermercado)
    for p in produtos:
        ProdutoCompra.objects.create(compra=compra,
                                     produto=p.produto,
                                     quantidade=p.quantidade,
                                     preco_unitario=p.produto.preco)
    return compra


def gerar_compra_agendada(consumidor, produtos, data):
    pass


def gerar_compra_recorrente(consumidor, produtos):
    pass


def custo_compras(supermercado, consumidor, produtosupermercados_map):
    preco_frete = regiao_service.preco_frete(supermercado, consumidor.usuario)
    return sum((x.preco * produtosupermercados_map[x] for x in produtosupermercados_map),
               start=preco_frete)
