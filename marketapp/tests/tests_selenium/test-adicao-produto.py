from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, random, datetime
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from marketapp.models import Supermercado, Categoria, Produto, ProdutoSupermercado

class TestAdicaoProduto(LiveServerTestCase):
    def setUp(self):
        super(TestAdicaoProduto, self).setUp()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = self.live_server_url
        self.verificationErrors = []
        self.user = self.gerar_usuario_cliente('lucasclient')
        self.supermercado = Supermercado.objects.create(usuario=self.gerar_usuario_cliente('super'), nome_exibicao='Villarreal', nome_url='villarreal')
        self.categoria = self.gerar_categoria('comida', 'foda-se descricao')
        self.gerar_produto_supermercado(self.gerar_produto_randomico('Cafe'))
        self.accept_next_alert = True
    
    def test_supermercado_table_exist(self):
        self.driver.get(self.base_url + "")
        table = self.driver.find_element_by_tag_name('table')
        self.assertIn("Supermercados", table.text)

    def gerar_usuario_cliente(self, name='usuario'):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return User.objects.create_user(username=name, password='123456')


    def gerar_produto_supermercado(self, produto, preco=10, quantidade=2, supermercado=None):
        if supermercado is None:
            return ProdutoSupermercado.objects.create(supermercado=self.supermercado,
                                                      produto=produto,
                                                      preco=preco,
                                                      quantidade=quantidade,
                                                      limite_venda=datetime.datetime(2014, 01, 01))
        return ProdutoSupermercado.objects.create(supermercado=supermercado,
                                                  produto=produto,
                                                  preco=preco,
                                                  quantidade=quantidade,
                                                  limite_venda=datetime.datetime(2014, 01, 01))


    def gerar_produto_randomico(self, nome='leite'):
        cod_barras = str(random.randint(0, 1000000000))
        return Produto.objects.create(nome=nome,
                                      categoria=self.categoria,
                                      quantidade=1,
                                      codigo_de_barras=cod_barras)

    
    def gerar_categoria(self, nome, descricao):
        return Categoria.objects.create(nome = nome, descricao = descricao)


    def test_adicao_produto(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Villarreal").click()
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys("lucasclient")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123456")
        driver.find_element_by_css_selector("button.primaryAction").click()
        produto = driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr[2]/td[1]").text
        driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr[2]/td[5]/a").click()
        assert driver.find_element_by_xpath("//table/tbody/tr[2]/td[1]").text == produto


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
