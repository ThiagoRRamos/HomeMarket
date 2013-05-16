'''
Created on May 9, 2013

@author: thiagorramos
'''
import requests


def validar_entrada(transacao_id, chave_acesso, **kwargs):
    endereco_post = "https://www.bcash.com.br/checkout/verify/"
    kwargs['transacao'] = transacao_id
    kwargs['token'] = chave_acesso
    resultado = requests.post(endereco_post, data=kwargs)
    return resultado.content == "VERIFICADO"
