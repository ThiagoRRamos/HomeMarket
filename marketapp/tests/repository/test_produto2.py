'''
Created on Apr 18, 2013

@author: Rhuan dos Anjos
'''
import datetime
import random

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from marketapp.repository.produto import get_produtos_que_estejam_em_dois_supermercados,\
    get_supermercados_produto 
from marketapp.models import Produto, Categoria, Supermercado, \
    ProdutoSupermercado


class TestProduto(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProduto, cls).setUpClass()
        cls.usuario = cls.gerar_usuario_cliente()
        cls.supermercado = Supermercado.objects.create(usuario=cls.gerar_usuario_cliente('super'),
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

    @classmethod
    def gerar_usuario_cliente(cls, name='usuario'):
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

    def gerar_supermercado(self,nome_exibicao):
        return Supermercado.objects.create(usuario=self.gerar_usuario_cliente("ola"),nome_exibicao=nome_exibicao)
    
    def gerar_produto_randomico(self):
        while 1:
            try:
                cod_barras = str(random.randint(0, 1000000000))
                return Produto.objects.create(categoria=self.categoria,
                                              quantidade=1,
                                              codigo_de_barras=cod_barras)
            except ValidationError:
                pass
            
    def teste_cria_supermercado_e_produto(self):
        supermercado1 = self.gerar_supermercado("Super1")
        produto_aleatorio1=self.gerar_produto_randomico()
        produto =self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado1)
        self.assertEqual("Super1", produto.supermercado.nome_exibicao)
        self.assertEqual(produto_aleatorio1,produto.produto)
        
    def mesmo_produto_em_2supermercados(self):
        supermercado1 = self.gerar_supermercado("Super1")
        supermercado2 = self.gerar_supermercado("Super2")
        produto_aleatorio1=self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado1)
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado2)
        self.assertTrue(supermercado1 in get_supermercados_produto(produto_aleatorio1))
        self.assertTrue(supermercado2 in get_supermercados_produto(produto_aleatorio1))
        self.assertTrue(produto_aleatorio1 in get_produtos_que_estejam_em_dois_supermercados(supermercado1,supermercado2))
        
    def mesmo_produto_em_apenas_2supermercados(self):
        supermercado1 = self.gerar_supermercado("Super1")
        supermercado2 = self.gerar_supermercado("Super2")
        supermercado3 = self.gerar_supermercado("Super3")
        produto_aleatorio1=self.gerar_produto_randomico()
        produto_aleatorio2=self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado1)
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado2)
        self.gerar_produto_supermercado(produto_aleatorio2,supermercado=supermercado3)
        self.assertTrue(supermercado1 in get_supermercados_produto(produto_aleatorio1))
        self.assertTrue(supermercado2 in get_supermercados_produto(produto_aleatorio1))
        self.assertFalse(supermercado3 in get_supermercados_produto(produto_aleatorio1))
        
    def varios_produtos_em_2supermercados(self):
        supermercado1 = self.gerar_supermercado("Super1")
        supermercado2 = self.gerar_supermercado("Super2")
        produto_aleatorio1=self.gerar_produto_randomico()
        produto_aleatorio2=self.gerar_produto_randomico()
        produto_aleatorio3=self.gerar_produto_randomico()
        produto_aleatorio4=self.gerar_produto_randomico()
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado1)
        self.gerar_produto_supermercado(produto_aleatorio1,supermercado=supermercado2)
        self.gerar_produto_supermercado(produto_aleatorio2,supermercado=supermercado1)
        self.gerar_produto_supermercado(produto_aleatorio2,supermercado=supermercado2)
        self.gerar_produto_supermercado(produto_aleatorio3,supermercado=supermercado1)
        self.gerar_produto_supermercado(produto_aleatorio4,supermercado=supermercado2)
        self.assertTrue(produto_aleatorio1 in get_produtos_que_estejam_em_dois_supermercados(supermercado1,supermercado2))
        self.assertTrue(produto_aleatorio2 in get_produtos_que_estejam_em_dois_supermercados(supermercado1,supermercado2))
        self.assertFalse(produto_aleatorio3 in get_produtos_que_estejam_em_dois_supermercados(supermercado1,supermercado2))
        self.assertFalse(produto_aleatorio4 in get_produtos_que_estejam_em_dois_supermercados(supermercado1,supermercado2))
        
