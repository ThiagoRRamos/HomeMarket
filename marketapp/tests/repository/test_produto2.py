'''
Created on Apr 18, 2013

@author: Rhuan dos Anjos
'''
import datetime
import random

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from marketapp.repository.produto import get_produtos_que_estejam_em_dois_supermercados, \
    get_supermercados_produto
from marketapp.models import Produto, Categoria, Supermercado, \
    ProdutoSupermercado
from marketapp.tests.utilidades.gerador import gerar_usuario_cliente, \
    gerar_produto_supermercado, gerar_produto_randomico, gerar_supermercado


class TestProduto(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProduto, cls).setUpClass()
        cls.usuario = gerar_usuario_cliente()
        cls.supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao="Supermercado")
        cls.categoria = Categoria.objects.create()

    @classmethod
    def tearDownClass(cls):
        cls.supermercado.delete()
        cls.categoria.delete()
        cls.usuario.delete()
        super(TestProduto, cls).tearDownClass()

    def setUp(self):
        super(TestProduto, self).setUp()

    def tearDown(self):
        super(TestProduto, self).tearDown()

    def gerar_produto_supermercado(self, produto, preco=10, quantidade=2, supermercado=None):
        if supermercado is None:
            return ProdutoSupermercado.objects.create(supermercado=self.supermercado,
                                                      produto=produto,
                                                      preco=preco,
                                                      quantidade=quantidade,
                                                      limite_venda=datetime.datetime(2014, 01, 01))
        return ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                  produto=produto,
                                                  preco=preco,
                                                  quantidade=quantidade,
                                                  limite_venda=datetime.datetime(2014, 01, 01))

    def teste_cria_supermercado_e_produto(self):
        supermercado1 = gerar_supermercado("Super1")
        produto_aleatorio1 = gerar_produto_randomico(categoria=self.categoria)
        produto = gerar_produto_supermercado(produto_aleatorio1,
                                             supermercado=supermercado1)
        self.assertEqual("Super1", produto.supermercado.nome_exibicao)
        self.assertEqual(produto_aleatorio1, produto.produto)

    def test_mesmo_produto_em_2supermercados(self):
        supermercado1 = gerar_supermercado("Super1")
        supermercado2 = gerar_supermercado("Super2")
        produto_aleatorio1 = gerar_produto_randomico(categoria=self.categoria)
        ps1 = gerar_produto_supermercado(produto_aleatorio1, supermercado=supermercado1)
        ps2 = gerar_produto_supermercado(produto_aleatorio1, supermercado=supermercado2)
        self.assertTrue(ps1 in get_supermercados_produto(produto_aleatorio1))
        self.assertTrue(ps2 in get_supermercados_produto(produto_aleatorio1))

    def test_mesmo_produto_em_apenas_2supermercados(self):
        supermercado1 = gerar_supermercado("Super1")
        supermercado2 = gerar_supermercado("Super2")
        supermercado3 = gerar_supermercado("Super3")
        produto_aleatorio1 = gerar_produto_randomico(categoria=self.categoria)
        produto_aleatorio2 = gerar_produto_randomico(categoria=self.categoria)
        ps1 = self.gerar_produto_supermercado(produto_aleatorio1, supermercado=supermercado1)
        ps2 = self.gerar_produto_supermercado(produto_aleatorio1, supermercado=supermercado2)
        ps3 = self.gerar_produto_supermercado(produto_aleatorio2, supermercado=supermercado3)
        dados = list(get_supermercados_produto(produto_aleatorio1))
        self.assertTrue(ps1 in dados)
        self.assertTrue(ps2 in dados)
        self.assertFalse(ps3 in dados)

