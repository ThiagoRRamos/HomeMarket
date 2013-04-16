from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from django.test import LiveServerTestCase
from django.contrib.auth.models import User

class TestAdicaoProduto(LiveServerTestCase):
    def setUp(self):
        super(TestAdicaoProduto, self).setUp()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = self.live_server_url
        self.verificationErrors = []
        self.user = User.objects.create_user('lucasclient', '', '123456')
        self.accept_next_alert = True
    
    def test_adicao_produto(self):
        driver = self.driver
        driver.get(self.base_url + "")
        driver.find_element_by_link_text("Villarreal").click()
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys("lucasclient")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123456")
        driver.find_element_by_css_selector("button.primaryAction").click()
        produto = driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr[3]/td[1]")
        driver.find_element_by_xpath("/html/body/div/div/table/tbody/tr[3]/td[5]/a").click()
        table = self.driver.find_element_by_tag_name('table')
        try: self.assertRegexpMatches(table.text, r"^[\s\S]*"+ produto.text +r"[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))

    
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
