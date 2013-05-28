'''
Created on May 28, 2013

@author: thiagorramos
'''
from django.test import TestCase
from marketapp.models import Supermercado, Categoria, PromocaoCombinacao, \
    ProdutoCarrinho
from marketapp.services.analisador_promocoes import promocoes_aplicaveis
from marketapp.services.carrinho import get_carrinho_usuario, adicionar_produto
from marketapp.tests.test_services.test_carrinho import TestCarrinho
from marketapp.tests.utilidades.gerador import gerar_usuario_cliente, \
    gerar_produto_randomico, gerar_produto_supermercado


class TestPromocoes(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPromocoes, cls).setUpClass()
        cls.usuario = gerar_usuario_cliente()
        cls.supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao="Supermercado")
        cls.categoria = Categoria.objects.create()

    @classmethod
    def tearDownClass(cls):
        cls.supermercado.delete()
        cls.categoria.delete()
        cls.usuario.delete()
        super(TestPromocoes, cls).tearDownClass()

    def setUp(self):
        super(TestPromocoes, self).setUp()

    def tearDown(self):
        super(TestPromocoes, self).tearDown()

    def testSemPromocao(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado1 = gerar_produto_supermercado(produto1,
                                                          supermercado=self.supermercado)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado2 = gerar_produto_supermercado(produto2,
                                                          supermercado=self.supermercado)
        produto3 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado3 = gerar_produto_supermercado(produto3,
                                                          supermercado=self.supermercado)
        a = list(promocoes_aplicaveis([produto_supermercado1,
                                       produto_supermercado2,
                                       produto_supermercado3],
                                      self.supermercado))
        self.assertEqual(len(a), 0)

    def testUmaPromocaoVazia(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado1 = gerar_produto_supermercado(produto1,
                                                          supermercado=self.supermercado)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado2 = gerar_produto_supermercado(produto2,
                                                          supermercado=self.supermercado)
        produto3 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado3 = gerar_produto_supermercado(produto3,
                                                          supermercado=self.supermercado)
        pc1 = adicionar_produto(self.usuario, produto_supermercado1)
        pc2 = adicionar_produto(self.usuario, produto_supermercado2)
        pc3 = adicionar_produto(self.usuario, produto_supermercado3)
        promocao1 = PromocaoCombinacao.objects.create(supermercado=self.supermercado,
                                                      desconto_percentual=50)
        a = list(promocoes_aplicaveis(get_carrinho_usuario(self.usuario).produtos.all(),
                                      self.supermercado))
        self.assertEqual(len(a), 1)

    def testUmaPromocao(self):
        produto1 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado1 = gerar_produto_supermercado(produto1,
                                                          supermercado=self.supermercado)
        produto2 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado2 = gerar_produto_supermercado(produto2,
                                                          supermercado=self.supermercado)
        produto3 = gerar_produto_randomico(categoria=self.categoria)
        produto_supermercado3 = gerar_produto_supermercado(produto3,
                                                          supermercado=self.supermercado)
        pc1 = adicionar_produto(self.usuario, produto_supermercado1)
        pc2 = adicionar_produto(self.usuario, produto_supermercado2)
        pc3 = adicionar_produto(self.usuario, produto_supermercado3)
        promocao1 = PromocaoCombinacao.objects.create(supermercado=self.supermercado,
                                                      desconto_percentual=50)
        promocao1.produtos.add(produto_supermercado1)
        a = list(promocoes_aplicaveis(get_carrinho_usuario(self.usuario).produtocarrinho_set.all(),
                                      self.supermercado))
        self.assertEqual(len(a), 1)
