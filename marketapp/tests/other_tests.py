from django.test import TestCase
from django.test.client import Client


class OtherTest(TestCase):
    def test_almost_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(7 + 1, 8)

    def test_open_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)