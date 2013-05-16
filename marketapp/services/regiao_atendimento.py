'''
Created on Apr 21, 2013

@author: thiagorramos
'''
from marketapp.models import RegiaoAtendida


def get_supermercados_que_atendem(usuario):
    cep = usuario.consumidor.cep
    for f in RegiaoAtendida.objects.filter(cep_inicio__lte=cep,
                                           cep_final__gte=cep):
        yield f.supermercado


def atende(supermercado, usuario):
    cep = usuario.consumidor.cep
    return RegiaoAtendida.objects.filter(supermercado=supermercado,
                                         cep_inicio__lte=cep,
                                         cep_final__gte=cep).exists()


def preco_frete(supermercado, usuario):
    cep = usuario.consumidor.cep
    return RegiaoAtendida.objects.get(supermercado=supermercado,
                                      cep_inicio__lte=cep,
                                      cep_final__gte=cep).preco


def tempo_entrega(supermercado, usuario):
    cep = usuario.consumidor.cep
    return RegiaoAtendida.objects.get(supermercado=supermercado,
                                      cep_inicio__lte=cep,
                                      cep_final__gte=cep).tempo_medio_entrega