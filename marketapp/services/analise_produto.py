'''
Created on May 16, 2013

@author: thiagorramos
'''
from marketapp.services.regiao_atendimento import get_supermercados_que_atendem
from marketapp.models import ProdutoSupermercado


def is_disponivel(produto, consumidor):
    supers = get_supermercados_que_atendem(consumidor.usuario)
    for su in supers:
        if ProdutoSupermercado.objects.filter(supermercado=su, produto=produto).exists():
            return True
    return False
