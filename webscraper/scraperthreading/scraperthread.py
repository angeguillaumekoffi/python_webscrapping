import threading
from ..scraper.produits_scraping import scrapingClass

def scraperthreadRunner():
    url = "https://www.marocannonces.com/maroc/telephones-portables--b359.html"
    running_threads_names = [t.name for t in threading.enumerate()]

    if not "thread_scraper" in running_threads_names:
        # On s'assure que le thread n'est pas deja en cours avant de le demarrer
        scraper = scrapingClass(url=url)
        # Demarrage du thread
        threading.Thread(name="thread_scraper", target=scraper.scraper_worker).start()
    return



