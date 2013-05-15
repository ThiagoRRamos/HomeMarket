'''
Created on May 15, 2013

@author: thiagorramos
'''
from marketapp.models import Compra, ProdutoCompra


def gerar_compra(consumidor,produtos):
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


def gerar_compra_agendada(consumidor,produtos, data):
    pass

def gerar_compra_recorrente(consumidor,produtos):
    pass