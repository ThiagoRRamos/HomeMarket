'''
Created on Apr 21, 2013

@author: thiagorramos
'''
from marketapp.models import RegiaoAtendida

def get_supermercados_que_atendem(usuario):
    cep = usuario.consumidor.cep
    return RegiaoAtendida.objects.filter(cep_inicio__lte=cep,cep_final__gte=cep).values('supermercado').distinct()