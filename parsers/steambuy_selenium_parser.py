import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from models import Game
from parsers.abstract_selenium_parser import AbstractSeleniumParser

class SteambuySeleniumParser(AbstractSeleniumParser):
    def search_games(self, query: str) -> List[Game]:
        url = f"https://steambuy.com/catalog/?q={query}"
        
        try:
            self.driver.get(url)
            
            # Ждем загрузки карточек товаров
            self.wait.until(
                EC.presence_of_element_located((By.ID, "product-list"))
            )
            
            # Даем время для полной загрузки AJAX
            time.sleep(2)
            
            return self.extract_products()
            
        except Exception as e:
            print(f"Ошибка Selenium: {e}")
            return []
    
    def _process_price(self, price_str: str) -> int:
        if "%" in price_str:
            return price_str.split("%")[1].replace("р", "").strip()
        return int("".join([l for l in price_str if l.isdigit()]))

    def _process_discount(self, discount_str: str) -> float:
        return float("".join([l for l in discount_str if l.isdigit()]))

    def extract_products(self) -> List[Game]:
        products = []
        
        # Ищем карточки товаров
        product_cards = self.driver.find_elements(By.CLASS_NAME, "product-item")
        
        for card in product_cards:
            try:
                product_data = Game(
                    title=self.get_text(card, '.product-item__title'),
                    price=self._process_price(self.get_text(card, '.product-item__price')),
                    url=self.get_attribute(card, 'a', 'href'),
                    discount=self._process_discount(self.get_text(card, '.product-item__discount')),
                    image=self.get_attribute(card, 'img', 'src')
                )
                products.append(product_data)
            except Exception as e:
                # print(f"Ошибка парсинга карточки: {e}")
                continue
        
        return products
