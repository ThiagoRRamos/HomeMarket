'''
Created on 28/05/2013

@author: User
'''
from marketapp.models import AvaliacaoSupermercado, Supermercado

def gerar_avaliacao_supermercado(nota, avaliacao, id_supermercado, consumidor):
    supermercado = Supermercado.objects.get(id = int(id_supermercado))
    avaliacaoSupermercado = AvaliacaoSupermercado.objects.create(nota = nota,
                                                                 avaliacao = avaliacao,
                                                                 supermercado = supermercado,
                                                                 consumidor = consumidor)
    return avaliacaoSupermercado