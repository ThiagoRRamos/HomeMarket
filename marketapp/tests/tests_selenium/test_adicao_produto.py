from django.test import LiveServerTestCase
from marketapp.models import Supermercado
from marketapp.tests.utilidades.gerador import gerar_produto_supermercado, \
    gerar_produto_randomico, gerar_usuario_cliente, gerar_categoria
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import unittest

class TestAdicaoProduto(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAdicaoProduto, cls).setUpClass()
        cls.user = gerar_usuario_cliente('lucasclient', password="123456")
        cls.supermercado = Supermercado.objects.create(usuario=gerar_usuario_cliente('super'),
                                                       nome_exibicao='Villa',
                                                       nome_url='villa')
        cls.categoria = gerar_categoria('comida', 'foda-se descricao')

    @classmethod
    def tearDownClass(cls):
        cls.supermercado.delete()
        cls.categoria.delete()
        cls.user.delete()
        super(TestAdicaoProduto, cls).tearDownClass()

    def setUp(self):
        super(TestAdicaoProduto, self).setUp()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = self.live_server_url
        self.verificationErrors = []
        gerar_produto_supermercado(gerar_produto_randomico(nome='Cafe',
                                                           categoria=self.categoria),
                                   supermercado=self.supermercado)
        self.accept_next_alert = True

    def test_supermercado_table_exist(self):
        self.driver.get(self.base_url + "")
        table = self.driver.find_element_by_tag_name('table')
        self.assertIn("Supermercados", table.text)

    def test_adicao_produto(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Villa").click()
        produto = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div[1]").text
        driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div[5]/a").click()
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys("lucasclient")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123456")
        driver.find_element_by_css_selector("button.primaryAction").click()
        assert driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]").text == produto

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
