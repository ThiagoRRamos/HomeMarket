from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestesSelenium(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_es_selenium(self):
        driver = self.driver
        driver.get(self.base_url + "")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def test_supermercado_table_exist(self):
        self.driver.get(self.base_url + "")
        table = self.driver.find_element_by_tag_name('table')
        self.assertIn("Supermercados", table.text)

if __name__ == "__main__":
    unittest.main()
