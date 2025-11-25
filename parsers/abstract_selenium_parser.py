from abc import ABC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome


class AbstractSeleniumParser(ABC):
    def __init__(self, driver: Chrome, wait: WebDriverWait) -> None:
        self.driver = driver
        self.wait = wait

    def get_text(self, element, selector):
        try:
            return element.find_element(By.CSS_SELECTOR, selector).text
        except:
            return ""
    
    def get_attribute(self, element, tag, attribute):
        try:
            return element.find_element(By.TAG_NAME, tag).get_attribute(attribute)
        except:
            return ""
    
    def close(self):
        self.driver.quit()