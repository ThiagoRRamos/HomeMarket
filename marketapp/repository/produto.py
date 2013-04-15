'''
Created on Apr 11, 2013

@author: thiagorramos
'''
from marketapp.models import Produto, ProdutoSupermercado
from django.db.models.query import QuerySet
QuerySet


def get_produtos_que_estejam_em_dois_supermercados(supermercado_um, supermercado_dois):
    ps1 = ProdutoSupermercado.objects.filter(supermercado=supermercado_um).order_by("produto__id")
    ps2 = ProdutoSupermercado.objects.filter(supermercado=supermercado_dois).order_by("produto__id")
    i1, i2 = 0, 0
    while i1 < len(ps1) and i2 < len(ps2):
        produto_supermercado_1 = ps1[i1]
        produto_supermercado_2 = ps2[i2]
        if produto_supermercado_1.produto.id < produto_supermercado_2.produto.id:
            i1 += 1
        elif produto_supermercado_1.produto.id > produto_supermercado_2.produto.id:
            i2 += 1
        else:
            yield {'produto': produto_supermercado_1.produto,
                   'ps1': produto_supermercado_1,
                   'ps2': produto_supermercado_2}
            i1+=1
            i2+=1
