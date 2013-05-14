from django.test import TestCase
from django.test.client import Client

class TestSupermercado(TestCase):
    def setUp(self):
    	super(TestSupermercado, self).setUp()
        self.client = Client()
        self.client.login(username='user-bretas', password='senha')

	def tearDown(self):
		super(TestSupermercado, self).tearDown()

    def test_regiao(self):
        response = self.client.get('/definir-regiao/')
        self.assertEqual(response.status_code, 200)
