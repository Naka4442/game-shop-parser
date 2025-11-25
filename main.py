from parsers.gabestore_selenium_parser import GabestoreSeleniumParser
from parsers.steambuy_selenium_parser import SteambuySeleniumParser
from parsers.steampay_parser import SteampayParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Фоновый режим
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    gabestore_parser = GabestoreSeleniumParser(driver, wait)
    steambuy_parser = SteambuySeleniumParser(driver, wait)
    steampay_parser = SteampayParser()
    while True:
        query = input("Игра: ")
        if query == "":
            break
        steambuy_games = steambuy_parser.search_games(query)
        print("____ Steambuy ____")
        for game in sorted(steambuy_games, key=lambda i: i.price):
            print(f"{game.title}: {game.price} ₽ [{game.discount}% скидка]")

        steampay_games = steampay_parser.search_games(query)
        print("____ Steampay ____")
        for game in sorted(steampay_games, key=lambda i: i.price):
            print(f"{game.title}: {game.price} ₽ [{game.discount}% скидка]")

        gabestore_games = gabestore_parser.search_games(query)
        print("____ Gabestore ____")
        for game in sorted(gabestore_games, key=lambda i: i.price):
            print(f"{game.title}: {game.price} ₽ [{game.discount}% скидка]")