from django.contrib.auth.models import User
from marketapp.services.carrinho import get_carrinho_usuario, adicionar_produto,\
    limpar_carrinho, CarrinhoComOutroSupermercado
from django.test import TestCase
from marketapp.models import Produto, Categoria, Supermercado, \
    ProdutoSupermercado
import datetime
import random


class TestCarrinho(TestCase):

    def setUp(self):
        super(TestCarrinho, self).setUp()
        self.usuario = self.gerar_usuario_cliente()
        self.supermercado = Supermercado.objects.create(usuario=self.gerar_usuario_cliente('super'))
        self.categoria = Categoria.objects.create()

    def gerar_usuario_cliente(self, name='usuario'):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return User.objects.create_user(username=name, password='senha')

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

    def gerar_produto_randomico(self):
        cod_barras = str(random.randint(0, 1000000000))
        return Produto.objects.create(categoria=self.categoria,
                                      quantidade=1,
                                      codigo_de_barras=cod_barras)

    def test_unicidade_carrinho(self):
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))

    def test_adicionar_produto_carrinho(self):
        produto = self.gerar_produto_randomico()
        produto_supermercado = self.gerar_produto_supermercado(produto)
        adicionar_produto(self.usuario, produto_supermercado)
        self.assertTrue(produto_supermercado in get_carrinho_usuario(self.usuario).produtos.all())

    def test_adicionar_varios_produtos_carrinho(self):
        produtos = [self.gerar_produto_randomico() for x in xrange(10)]
        pss = [self.gerar_produto_supermercado(p) for p in produtos]
        for ps in pss:
            adicionar_produto(self.usuario, ps)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 10)
        for ps in pss:
            self.assertTrue(ps in get_carrinho_usuario(self.usuario).produtos.all())

    def test_limpar_carrinho(self):
        produto = self.gerar_produto_randomico()
        produto_supermercado = self.gerar_produto_supermercado(produto)
        adicionar_produto(self.usuario, produto_supermercado)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 1)
        limpar_carrinho(self.usuario)
        self.assertEqual(len(get_carrinho_usuario(self.usuario).produtos.all()), 0)

    def test_supermercado_errado_produto_novo(self):
        produto1 = self.gerar_produto_randomico()
        produto2 = self.gerar_produto_randomico()
        ps1 = self.gerar_produto_supermercado(produto1)
        supermercado2 = Supermercado.objects.create(usuario=self.gerar_usuario_cliente("ola"))
        ps2 = self.gerar_produto_supermercado(produto2,supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        try:
            adicionar_produto(self.usuario, ps2)
            self.fail("Excecao deveria ter sido gerada")
        except CarrinhoComOutroSupermercado:
            pass

    def test_supermercado_errado_mesmo_produto(self):
        produto1 = self.gerar_produto_randomico()
        ps1 = self.gerar_produto_supermercado(produto1)
        supermercado2 = Supermercado.objects.create(usuario=self.gerar_usuario_cliente("ola"))
        ps2 = self.gerar_produto_supermercado(produto1,supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        try:
            adicionar_produto(self.usuario, ps2)
            self.fail("Excecao deveria ter sido gerada")
        except CarrinhoComOutroSupermercado:
            pass

    def test_supermercado_errado_pessoas_diferentes(self):
        produto1 = self.gerar_produto_randomico()
        ps1 = self.gerar_produto_supermercado(produto1)
        supermercado2 = Supermercado.objects.create(usuario=self.gerar_usuario_cliente("ola"))
        ps2 = self.gerar_produto_supermercado(produto1,supermercado=supermercado2)
        adicionar_produto(self.usuario, ps1)
        adicionar_produto(supermercado2.usuario, ps2)
