'''
Created on May 27, 2013

@author: thiagorramos
'''


def promocoes_supermercado(supermercado):
    from marketapp.models import PromocaoCombinacao, PromocaoSimples, PromocaoAtacado
    for pro in PromocaoCombinacao.objects.filter(supermercado=supermercado).distinct():
        yield pro
    for prom in PromocaoSimples.objects.filter(supermercado=supermercado).distinct():
        yield prom
    for promo in PromocaoAtacado.objects.filter(supermercado=supermercado).distinct():
        yield promo


def promocoes_aplicaveis(produtos, supermercado):
    promo = promocoes_supermercado(supermercado)
    mapa_produtos = {p.produto: p.quantidade for p in produtos}
    for p in promo:
        if promocao_valida(p, mapa_produtos):
            yield p
            if not p.cumulativa:
                decrementar_por_promocao(p, mapa_produtos)


def desconto_promocao(promocao):
    a = sum(x.preco for x in promocao.get_produtos)
    return float(promocao.desconto_percentual) * float(a) / 100.0


def desconto_promocoes(promocoes):
    return sum(desconto_promocao(p) for p in promocoes)


def promocao_valida(promocao, mapa_produtos):
    return promocao.se_aplica(mapa_produtos)


def decrementar_por_promocao(promocao, mapa_produtos):
    for p in promocao.get_produtos():
        mapa_produtos[p] -= 1
