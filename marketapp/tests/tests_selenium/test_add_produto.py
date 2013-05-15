from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from django.test import LiveServerTestCase
import unittest
from marketapp.models import Supermercado, Categoria, Produto
from marketapp.tests.utilidades.gerador import gerar_categoria,\
    gerar_usuario_cliente

class TestAddProduto(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAddProduto, cls).setUpClass()
        cls.user = gerar_usuario_cliente('lucasclient')
        cls.supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao='Villarreal',
                                                       nome_url='villarreal')
        cls.categoria = gerar_categoria('Categoria Especial', 'foda-se descricao')

    @classmethod
    def tearDownClass(cls):
        cls.supermercado.delete()
        cls.categoria.delete()
        cls.user.delete()
        super(TestAddProduto, cls).tearDownClass()

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = self.live_server_url
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_add_produto(self):
        driver = self.driver
        driver.get(self.base_url + "/criar_produto/")
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys("super")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("senha")
        driver.find_element_by_css_selector("button.primaryAction").click()
        driver.find_element_by_id("id_nome").send_keys("Van")
        driver.find_element_by_id("id_descricao").clear()
        driver.find_element_by_id("id_descricao").send_keys("Van muito louca")
        driver.find_element_by_id("id_marca").clear()
        driver.find_element_by_id("id_marca").send_keys("Wolks")
        driver.find_element_by_id("id_codigo_de_barras").clear()
        driver.find_element_by_id("id_codigo_de_barras").send_keys("1323214324")
        Select(driver.find_element_by_id("id_categoria")).select_by_visible_text("Categoria Especial")
        driver.find_element_by_id("id_quantidade").clear()
        driver.find_element_by_id("id_quantidade").send_keys("1")
        Select(driver.find_element_by_id("id_quantidade_unidade")).select_by_visible_text("un")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        Produto.objects.get(codigo_de_barras="1323214324")
        
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
