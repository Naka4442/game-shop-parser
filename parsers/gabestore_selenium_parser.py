import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from models.game import Game
from parsers.abstract_selenium_parser import AbstractSeleniumParser


class GabestoreSeleniumParser(AbstractSeleniumParser):
    def search_games(self, query: str):
        self.driver.get("https://gabestore.ru/")
        self.wait.until(EC.presence_of_element_located((By.NAME, "search")))
        
        self.driver.find_element(By.NAME, "search").click()
        self.driver.find_element(By.NAME, "search").send_keys(query)
        self.driver.find_element(By.CLASS_NAME, "search-btn").click()

        # Ждем загрузки карточек товаров
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shop-item")))

        # Даем время для полной загрузки AJAX
        time.sleep(2)

        return self.extract_products()
    
    def _process_discount(self, discount_str: str) -> float:
        return float("".join([l for l in discount_str if l.isdigit()]))

    def _process_price(self, price_str: str) -> int:
        if "%" in price_str:
            return price_str.split("%")[1].replace("₽", "").strip()
        return int("".join([l for l in price_str if l.isdigit()]))

    def extract_products(self) -> List[Game]:
        products = []
        
        # Ищем карточки товаров
        product_cards = self.driver.find_elements(By.CSS_SELECTOR, ".b-search-result__wrapper .shop-item")
        
        for card in product_cards:
            try:
                product_data = Game(
                    title=self.get_text(card, '.shop-item__name'),
                    price=self._process_price(self.get_text(card, '.shop-item__price-current')),
                    url=self.get_attribute(card, 'a', 'href'),
                    discount=self._process_discount(self.get_text(card, '.shop-item__price-discount')),
                    image_url=self.get_attribute(card, 'img', 'src')
                )
                products.append(product_data)
            except Exception as e:
                print(f"Ошибка парсинга карточки: {e}")
                continue
        
        return products
        