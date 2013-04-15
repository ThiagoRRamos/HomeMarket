from django.test import TestCase
from django.test.client import Client
from marketapp.tests.other_tests import OtherTest


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_open_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
