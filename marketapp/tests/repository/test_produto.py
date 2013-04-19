'''
Created on Apr 11, 2013

@author: thiagorramos
'''
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import unittest
from marketapp.models import Supermercado, ProdutoSupermercado, Produto, \
    Categoria
from marketapp.repository.produto import \
    get_produtos_que_estejam_em_dois_supermercados
import datetime
import random


class TestProdutoRepository(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProdutoRepository, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestProdutoRepository, cls).tearDownClass()

    def setUp(self):
        super(TestProdutoRepository, self).setUp()
        user1 = User.objects.create_user("a", "email", "password")
        user2 = User.objects.create_user("b", "email2", "password")
        self.super1 = Supermercado.objects.create(usuario=user1)
        self.super2 = Supermercado.objects.create(usuario=user2)
        self.categoria = Categoria.objects.create()

    def gerar_produto_supermercado(self, produto, preco=10, quantidade=2, supermercado=None):
        return ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                  produto=produto,
                                                  preco=preco,
                                                  quantidade=quantidade,
                                                  limite_venda=datetime.datetime(2014, 01, 01))

    def tearDown(self):
        super(TestProdutoRepository, self).tearDown()

    def testProdutoEmDoisSupermercadosVazio(self):
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosSomenteUmSupermercado(self):
        produto1 = self.gerar_produto_randomico()
        produto2 = self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto1, supermercado=self.super1)
        self.gerar_produto_supermercado(produto2, supermercado=self.super1)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosProdutosDiferentes(self):
        produto1 = self.gerar_produto_randomico()
        produto2 = self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto1, supermercado=self.super1)
        self.gerar_produto_supermercado(produto2, supermercado=self.super2)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosUmProduto(self):
        produto1 = self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto1, supermercado=self.super1)
        self.gerar_produto_supermercado(produto1, supermercado=self.super2)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]['produto'], produto1)
    def gerar_produto_randomico(self):
        while 1:
            try:
                cod_barras = str(random.randint(0, 1000000000))
                return Produto.objects.create(categoria=self.categoria,
                                              quantidade=1,
                                              codigo_de_barras=cod_barras)
            except ValidationError:
                pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
