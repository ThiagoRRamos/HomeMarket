'''
Created on Jun 11, 2013

@author: thiagorramos
'''

from django.test import TestCase
from marketapp.models import PromocaoCombinacao, ProdutoSupermercado,\
    RegiaoAtendida
from marketapp.tests.utilidades.gerador import gerar_supermercado, \
    gerar_produto_randomico, gerar_categoria, gerar_usuario_cliente
from marketapp.services.marketing import consumidores_promocao


class TestMarketing(TestCase):

    def test_sem_clientes_promocao(self):
        supermercado = gerar_supermercado("A")
        categoria = gerar_categoria("a", "B")
        produto = gerar_produto_randomico(categoria=categoria)
        produtosupemercado = ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                                produto=produto,
                                                                preco=10,
                                                                quantidade=10)
        promocao = PromocaoCombinacao.objects.create(supermercado=supermercado,
                                                     desconto_percentual=10)
        promocao.produtos.add(produtosupemercado)
        cons = list(consumidores_promocao(promocao))
        self.assertEqual(len(cons), 0)

    def test_um_cliente_promocao(self):
        supermercado = gerar_supermercado("Q")
        RegiaoAtendida.objects.create(cep_inicio="00000-000",
                                      cep_final=" 99999-999",
                                      supermercado=supermercado,
                                      preco=5,
                                      tempo=5)
        gerar_usuario_cliente("testador")
        categoria = gerar_categoria("L", "B")
        produto = gerar_produto_randomico(categoria=categoria)
        produtosupemercado = ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                                produto=produto,
                                                                preco=10,
                                                                quantidade=10)
        promocao = PromocaoCombinacao.objects.create(supermercado=supermercado,
                                                     desconto_percentual=10)
        promocao.produtos.add(produtosupemercado)
        cons = list(consumidores_promocao(promocao))
        self.assertEqual(len(cons), 0)

    def test_dois_clientes_promocao(self):
        supermercado = gerar_supermercado("A")
        categoria = gerar_categoria("a", "B")
        produto = gerar_produto_randomico(categoria=categoria)
        produtosupemercado = ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                                produto=produto,
                                                                preco=10,
                                                                quantidade=10)
        promocao = PromocaoCombinacao.objects.create(supermercado=supermercado,
                                                     desconto_percentual=10)
        promocao.produtos.add(produtosupemercado)
        cons = list(consumidores_promocao(promocao))
        self.assertEqual(len(cons), 0)