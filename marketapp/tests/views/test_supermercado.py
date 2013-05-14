from django.test import TestCase
from django.test.client import Client

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
