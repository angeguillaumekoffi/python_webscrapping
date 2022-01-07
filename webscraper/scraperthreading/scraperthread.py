import threading
from ..scraper.produits_scraping import scrapingClass

def scraperthreadRunner():
    url = "https://www.marocannonces.com/maroc/telephones-portables--b359.html"
    for t in threading.enumerate():
        if not t.is_alive():
            scraper = scrapingClass(url=url)
            # Demarrage du thread
            threading.Thread(name=f'Thread du scraper', target=scraper.scraper_worker).start()

    return



