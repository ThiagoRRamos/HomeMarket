'''
Created on Apr 19, 2013

@author: thiagorramos
'''
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from marketapp.models import ProdutoSupermercado, Produto, Supermercado, \
    Categoria
import random


def gerar_produto_supermercado(produto, preco=10, quantidade=2, supermercado=None):
    return ProdutoSupermercado.objects.create(supermercado=supermercado,
                                              produto=produto,
                                              preco=preco,
                                              quantidade=quantidade)


def gerar_produto_randomico(**kwargs):
        dados = {"quantidade": 1,
                 "codigo_de_barras": "0"}
        dados.update(kwargs)
        while 1:
            try:
                dados['codigo_de_barras'] = str(random.randint(0, 1000000000))
                return Produto.objects.create(**dados)
            except ValidationError:
                pass


def gerar_supermercado(nome_exibicao):
        return Supermercado.objects.create(usuario=gerar_usuario_cliente(nome_exibicao),
                                           nome_exibicao=nome_exibicao)

def gerar_categoria(nome, descricao):
    return Categoria.objects.create(nome=nome, descricao=descricao)

def gerar_usuario_cliente(name='usuario',password="senha"):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return User.objects.create_user(username=name, password=password)