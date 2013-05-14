from django.test import TestCase
from django.test.client import Client
from marketapp.models import Compra
from django.contrib.auth.models import User

class TestSupermercado(TestCase):
    def setUp(self):
        super(TestSupermercado, self).setUp()
        self.client = Client()

    def tearDown(self):
        super(TestSupermercado, self).tearDown()

    def test_regiao_supermercado_logado(self):
        self.client.login(username='user-bretas', password='senha')
        response = self.client.get('/definir-regiao/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_regiao_supermercado_nao_logado(self):
        response = self.client.get('/definir-regiao/')
        self.assertEqual(response.status_code, 302)

    def test_regiao_supermercado_nao_supermercado(self):
    	self.client.login(username='cliente', password='senha')
        response = self.client.get('/definir-regiao/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_atualizacao_status(self):
        usuario = User.objects.get(username='user-extra')
        usuario_c = User.objects.get(username='cliente')
        self.client.login(username='user-extra',password='senha')
        c = Compra.objects.create(supermercado=usuario.supermercado,
                                  consumidor=usuario_c.consumidor,
                                  status_pagamento='pn')
        self.assertEqual(c.status_pagamento,'pn')
        a = '/atualizar-compra/'+str(c.id)+'?status=pd'
        print a
        r = self.client.get(a)
        print r.status_code
        compra = Compra.objects.get()
        self.assertEqual(compra.status_pagamento,'pd')