'''
Created on Apr 11, 2013

@author: thiagorramos
'''
from django.test import TestCase
from django.utils import unittest
from marketapp.models import Supermercado


class TestProdutoRepository(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestProdutoRepository, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestProdutoRepository, cls).tearDownClass()

    def setUp(self):
        super(TestProdutoRepository, self).setUp()
        self.super1 = Supermercado.objects.create()
        self.super2 = Supermercado.objects.create()

    def tearDown(self):
        super(TestProdutoRepository, self).tearDown()

    def testProdutoEmDoisSupermercadosVazio(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
