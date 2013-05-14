'''
Created on Apr 5, 2013

@author: thiagorramos
'''
from django.test import TestCase
from django.contrib.auth.models import User
from marketapp.models import Consumidor, Compra, CarrinhoCompras
from marketapp.services.carrinho import get_carrinho_usuario

class TestCliente(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        u = User.objects.create_user(username='cliente-teste', password='senha')
        self.usuario = u
        Consumidor.objects.create(usuario=u,
                                  cep='55555-001')
        self.client.login(username='cliente-teste', password='senha')
    
    def testHome(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def testHomeCliente(self):
        response = self.client.get('/home-cliente/')
        self.assertEqual(response.status_code, 200)
        
    def testHomeSupermercado(self):
        response = self.client.get('/home-supermercado/')
        self.assertEqual(response.status_code, 302)
        
    def testCompra(self):
        response = self.client.get('/colocar-no-carrinho/4')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Compra.objects.filter(consumidor=self.usuario.consumidor).exists())
        self.client.get('/comprar/')
        self.assertTrue(Compra.objects.filter(consumidor=self.usuario.consumidor).exists())
        compra = Compra.objects.filter(consumidor=self.usuario.consumidor)[0]
        self.assertEqual(len(compra.produtos.all()), 1)
        self.assertEqual(compra.status_pagamento, 'pn')
        self.client.get('/comprar/dinheiro/' + str(compra.id))
        compra = Compra.objects.filter(consumidor=self.usuario.consumidor)[0]
        self.assertEqual(compra.status_pagamento, 'pd')
