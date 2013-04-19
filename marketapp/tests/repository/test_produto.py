'''
Created on Apr 11, 2013

@author: thiagorramos
'''
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import unittest
from marketapp.models import Supermercado, Categoria
from marketapp.repository.produto import get_produtos_que_estejam_em_dois_supermercados
from marketapp.tests.utilidades.gerador import gerar_produto_supermercado, \
    gerar_produto_randomico


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

    def tearDown(self):
        super(TestProdutoRepository, self).tearDown()

    def testProdutoEmDoisSupermercadosVazio(self):
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosSomenteUmSupermercado(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        gerar_produto_supermercado(produto1, supermercado=self.super1)
        gerar_produto_supermercado(produto2, supermercado=self.super1)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosProdutosDiferentes(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        gerar_produto_supermercado(produto1, supermercado=self.super1)
        gerar_produto_supermercado(produto2, supermercado=self.super2)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 0)

    def testProdutoEmDoisSupermercadosUmProduto(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        gerar_produto_supermercado(produto1, preco=20, supermercado=self.super1)
        gerar_produto_supermercado(produto1, preco=10, supermercado=self.super2)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]['produto'], produto1)
        self.assertEqual(dados[0]['ps1'].preco, 20)
        self.assertEqual(dados[0]['ps2'].preco, 10)

    def testProdutoEmDoisSupermercadosAlgunsProduto(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        produto3 = gerar_produto_randomico(categoria=self.categoria)
        produto4 = gerar_produto_randomico(categoria=self.categoria)
        produto5 = gerar_produto_randomico(categoria=self.categoria)
        gerar_produto_supermercado(produto1, supermercado=self.super1)
        gerar_produto_supermercado(produto2, supermercado=self.super1)
        gerar_produto_supermercado(produto3, supermercado=self.super1)
        gerar_produto_supermercado(produto2, supermercado=self.super2)
        gerar_produto_supermercado(produto3, supermercado=self.super2)
        gerar_produto_supermercado(produto4, supermercado=self.super2)
        gerar_produto_supermercado(produto5, supermercado=self.super2)
        dados = list(get_produtos_que_estejam_em_dois_supermercados(self.super1, self.super2))
        self.assertEqual(len(dados), 2)
        for da in dados:
            self.assertTrue(da['produto'] in [produto2, produto3])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
