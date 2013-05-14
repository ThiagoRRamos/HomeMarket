'''
Created on 13/05/2013

@author: User
'''
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from marketapp.services.carrinho import get_carrinho_usuario, adicionar_produto, \
    limpar_carrinho, CarrinhoComOutroSupermercado
from marketapp.models import Produto, Categoria, Supermercado,RegiaoAtendida, ProdutoSupermercado
    
from marketapp.tests.utilidades.gerador import gerar_usuario_cliente, \
    gerar_produto_randomico, gerar_produto_supermercado, gerar_regiao



class TestRegiao(TestCase):
   
    
    def testSuperMarketInRegiao(self):
       usuario = gerar_usuario_cliente()
       supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao="Supermercado")
       regiao = gerar_regiao(supermercado = supermercado)
       Inicio = regiao.cep_inicio.split("-")
       cep = usuario.consumidor.cep.split("-")
       Fim = regiao.cep_final.split("-")
       self.assertTrue(int(Inicio[0]) < int(cep[0]))
       self.assertTrue(int(Fim[0]) < int(cep[0]))
       
     
    