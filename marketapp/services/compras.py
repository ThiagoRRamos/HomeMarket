'''
Created on May 15, 2013

@author: thiagorramos
'''
from marketapp.models import Compra, ProdutoCompra, CompraAgendada, \
    ProdutoCompraAgendada, CompraRecorrente, ProdutoCompraRecorrente
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
    supermercado = produtos[0].produto.supermercado
    compra = CompraAgendada.objects.create(modo_pagamento='nn',
                                   status_pagamento='pn',
                                   consumidor=consumidor,
                                   supermercado=supermercado,
                                   data_entrega=data)
    for p in produtos:
        ProdutoCompraAgendada.objects.create(compra=compra,
                                     produto=p.produto,
                                     quantidade=p.quantidade,
                                     preco_unitario=p.produto.preco)
    return compra


def gerar_compra_recorrente(consumidor, produtos, frequencia):
    supermercado = produtos[0].produto.supermercado
    compra = CompraRecorrente.objects.create(modo_pagamento='nn',
                                   status_pagamento='pn',
                                   consumidor=consumidor,
                                   supermercado=supermercado,
                                   frequencia=frequencia)
    for p in produtos:
        ProdutoCompraRecorrente.objects.create(compra=compra,
                                     produto=p.produto,
                                     quantidade=p.quantidade,
                                     preco_unitario=p.produto.preco)
    return compra


def custo_compras(supermercado, consumidor, produtosupermercados_map):
    preco_frete = regiao_service.preco_frete(supermercado, consumidor.usuario)
    return sum((x.preco * produtosupermercados_map[x] for x in produtosupermercados_map),
               start=preco_frete)
