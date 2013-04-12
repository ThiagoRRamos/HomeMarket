from django.contrib.auth.models import User
from marketapp.services.carrinho import get_carrinho_usuario, adicionar_produto
from django.test import TestCase
from marketapp.models import Produto, Categoria, Supermercado, \
    ProdutoSupermercado
import datetime


class TestCarrinho(TestCase):

    def setUp(self):
        super(TestCarrinho, self).setUp()
        self.usuario = self.gerar_usuario_cliente()

    def gerar_usuario_cliente(self, name='usuario'):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return User.objects.create_user(username=name, password='senha')

    def test_unicidade_carrinho(self):
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))
        carrinho = get_carrinho_usuario(self.usuario)
        self.assertEqual(carrinho, get_carrinho_usuario(self.usuario))

    def test_adicionar_produto_carrinho(self):
        supermercado = Supermercado.objects.create(usuario=self.gerar_usuario_cliente('super'))
        categoria = Categoria.objects.create()
        produto = Produto.objects.create(categoria=categoria,
                                         quantidade=1)
        produto_supermercado = ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                                  produto=produto,
                                                                  preco=13.22,
                                                                  quantidade=3,
                                                                  limite_venda=datetime.datetime(2014, 01, 01))
        adicionar_produto(self.usuario, produto_supermercado)
        self.assertTrue(produto_supermercado in get_carrinho_usuario(self.usuario).produtos.all())