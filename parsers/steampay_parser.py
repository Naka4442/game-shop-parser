from typing import List
from bs4 import BeautifulSoup, Tag
import requests

from models.game import Game


class SteampayParser:
    
    STEAMBUY_URL = "https://steampay.com"

    def _process_title(self, title: str) -> str:
        return title.split("\n")[0].strip()

    def _process_price(self, price_str: str) -> int:
        if "%" in price_str:
            return price_str.split("%")[1].replace("₽", "").strip()
        return int("".join([l for l in price_str if l.isdigit()]))

    def _process_discount(self, discount_str: str) -> float:
        return float("".join([l for l in discount_str if l.isdigit()]))

    def _parse_game(self, item: Tag) -> Game:
        title = self._process_title(item.select_one(".catalog-item__name").text.strip())
        price = self._process_price(item.select_one(".catalog-item__price").get_text(strip=True))
        url = item.get("href")
        discount = self._process_discount(item.select_one(".catalog-item__discount").text.strip())
        return Game(title=title, price=int(price), url=url, discount=discount)
    
    def search_games(self, query: str) -> List[Game]:
        site = requests.get(f"{self.STEAMBUY_URL}/search?q={query}").content
        soup = BeautifulSoup(site, "html.parser")
        items = soup.find_all("a", class_="catalog-item")
        games = []
        for item in items:
            try:
                games.append(self._parse_game(item))
            except ValueError as e:
                # print(f"Ошибка парсинга: {item}: {e}")
                continue
        return games

if __name__ == "__main__":
    parser = SteampayParser()
    games = parser.search_games(input("Игра: "))
    for game in sorted(games, key=lambda i: i.price):
        print(f"{game.title}: {game.price} ₽ [{game.discount}% скидка]")
