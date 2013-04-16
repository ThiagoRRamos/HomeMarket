from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class TestAddProduto(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = true
    
    def test_add_produto(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Villarreal").click()
        driver.find_element_by_id("id_login").click()
        driver.find_element_by_id("id_login").clear()
        driver.find_element_by_id("id_login").send_keys("lucascliente")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("123456")
        driver.find_element_by_css_selector("button.primaryAction").click()
        # Warning: verifyTextPresent may require manual changes
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Leite[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        # ERROR: Caught exception [ERROR: Unsupported command [isTextPresent | Leite | ]]
        driver.find_element_by_xpath("(//a[contains(text(),'Adicionar ao Carrinho')])[2]").click()
        # Warning: verifyTextPresent may require manual changes
        try: self.assertRegexpMatches(driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*Leite[\s\S]*$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        # ERROR: Caught exception [ERROR: Unsupported command [isTextPresent | Leite | ]]
    
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
