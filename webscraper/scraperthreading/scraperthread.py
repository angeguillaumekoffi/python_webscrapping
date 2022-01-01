import threading
from ..scraper.produits_scraping import scrapingClass
import time

def scraperthreadRunner():
    url = "https://www.marocannonces.com/maroc/telephones-portables--b359.html"
    scraper = scrapingClass(url=url)

    # Demarrage du thread
    threading.Thread(name=f'Thread du scraper', target=scraper.startscraper).start()

    return



