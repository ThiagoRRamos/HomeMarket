'''
Created on May 27, 2013

@author: thiagorramos
'''
from collections import Counter


def promocoes_supermercado(supermercado):
    from marketapp.models import PromocaoCombinacao
    for pro in PromocaoCombinacao.objects.filter(supermercado=supermercado).distinct():
        yield pro


def promocoes_aplicaveis(produtos, supermercado):
    promo = promocoes_supermercado(supermercado)
    mapa_produtos = {p.produto: p.quantidade for p in produtos}
    for p in promo:
        if promocao_valida(p, mapa_produtos):
            yield p
            if not p.cumulativa:
                decrementar_por_promocao(p, mapa_produtos)


def desconto_promocao(promocao, produtos):
    a = sum(x.produto.preco for x in produtos)
    return float(promocao.desconto_percentual) * float(a) / 100.0


def desconto_promocoes(promocoes, produtos):
    return sum(desconto_promocao(p, produtos) for p in promocoes)


def promocao_valida(promocao, mapa_produtos):
    for p in promocao.produtos.all():
        if p not in mapa_produtos or mapa_produtos[p] == 0:
            return False
    return True


def decrementar_por_promocao(promocao, mapa_produtos):
    for p in promocao.produtos.all():
        mapa_produtos[p] -= 1
