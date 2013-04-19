import datetime
import random

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from marketapp.services.carrinho import get_carrinho_usuario, adicionar_produto, \
    limpar_carrinho, CarrinhoComOutroSupermercado
from marketapp.models import Produto, Categoria, Supermercado, \
    ProdutoSupermercado
from marketapp.tests.utilidades.gerador import gerar_usuario_cliente, \
    gerar_produto_randomico, gerar_produto_supermercado


class TestCarrinho(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCarrinho, cls).setUpClass()
        cls.usuario = gerar_usuario_cliente()
        cls.supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao="Supermercado")
        cls.categoria = Categoria.objects.create()

    @classmethod
    def tearDownClass(cls):
        cls.supermercado.delete()
        cls.categoria.delete()
        cls.usuario.delete()
        super(TestCarrinho, cls).tearDownClass()

    def setUp(self):
        super(TestCarrinho, self).setUp()

    def tearDown(self):
        super(TestCarrinho, self).tearDown()

    def test_unicidade_carrinho(self):
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))

    def test_adicionar_produto_carrinho(self):
        produto = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado = gerar_produto_supermercado(produto,
                                                          supermercado=self.supermercado)
        adicionar_produto(self.usuario, produto_supermercado)
        self.assertTrue(produto_supermercado in get_carrinho_usuario(self.usuario).produtos.all())

    def test_adicionar_varios_produtos_carrinho(self):
        produtos = [gerar_produto_randomico(categoria=self.categoria) for x in xrange(10)]
        pss = [gerar_produto_supermercado(p,supermercado=self.supermercado) for p in produtos]
        for ps in pss:
            adicionar_produto(self.usuario, ps)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 10)
        for ps in pss:
            self.assertTrue(ps in get_carrinho_usuario(self.usuario).produtos.all())

    def test_limpar_carrinho(self):
        produto = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado = gerar_produto_supermercado(produto,
                                                          supermercado=self.supermercado)
        adicionar_produto(self.usuario, produto_supermercado)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 1)
        limpar_carrinho(self.usuario)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 0)

    def test_supermercado_errado_produto_novo(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        ps1 = gerar_produto_supermercado(produto1,
                                         supermercado=self.supermercado)
        supermercado2 = Supermercado.objects.create(usuario=gerar_usuario_cliente("ola"))
        ps2 = gerar_produto_supermercado(produto2, supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        try:
            adicionar_produto(self.usuario, ps2)
            self.fail("Excecao deveria ter sido gerada")
        except CarrinhoComOutroSupermercado:
            pass

    def test_supermercado_errado_mesmo_produto(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        ps1 = gerar_produto_supermercado(produto1,
                                         supermercado=self.supermercado)
        supermercado2 = Supermercado.objects.create(usuario=gerar_usuario_cliente("ola"))
        ps2 = gerar_produto_supermercado(produto1,
                                         supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        try:
            adicionar_produto(self.usuario, ps2)
            self.fail("Excecao deveria ter sido gerada")
        except CarrinhoComOutroSupermercado:
            pass

    def test_supermercado_errado_pessoas_diferentes(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        ps1 = gerar_produto_supermercado(produto1, supermercado=self.supermercado)
        supermercado2 = Supermercado.objects.create(usuario=gerar_usuario_cliente("ola"))
        ps2 = gerar_produto_supermercado(produto1, supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        adicionar_produto(supermercado2.usuario, ps2)
