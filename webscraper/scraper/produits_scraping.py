from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, datetime
from ..models import Produit

class scrapingClass:
    def __init__(self, url):
        self._url = url
        self.liste_conteneur_li = []
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("headless")
        self._browser = webdriver.Chrome(ChromeDriverManager().install(), options=self._options)
        return

    def startscraper(self):
        self._browser.get(url=str(self._url))

        # Bouton suivant de pagination
        btn_suivant = self._browser.find_element(By.XPATH, "//li[@class='next']/a")

        self.scrap(browser=self._browser)

        url_page_suivante = btn_suivant.get_attribute("href")
        num_page_suivante = int(url_page_suivante.split("pge=")[-1])
        num_page_actuelle = 1

        while (num_page_actuelle < num_page_suivante):
            self._browser.get(url=url_page_suivante)
            self.scrap(browser=self._browser)

            # initialisation des elements de la page suivante
            url_page_suivante = self._browser.find_element(By.XPATH, "//li[@class='next']/a").get_attribute("href")
            num_page_actuelle = num_page_suivante
            num_page_suivante = int(url_page_suivante.split("pge=")[-1])

            print("Page actuelle == ", num_page_actuelle)
            time.sleep(300)

        self._browser.quit()
        return

    def scrap(self, browser):
        """ Methode permettant de recuperer les données à partir du code html et les sauvegarder """

        liste_ul = browser.find_element(By.CLASS_NAME, 'cars-list')
        self.liste_conteneur_li = liste_ul.find_elements(By.CSS_SELECTOR, 'li:not(class)')
        self.liste_conteneur_li.append(liste_ul.find_element(By.CLASS_NAME, 'firstitem'))  # On recupère tous les conteneurs d'articles sauf celui de la publicité

        for elemnt in self.liste_conteneur_li:
            image = self.getAttribut(element=elemnt, by="CN", by_value='lazy', attrib="data-original")
            titre = self.getValue(element=elemnt, by="TN", by_value='h3')
            prix = self.getValue(element=elemnt, by="CN", by_value='price')
            ville = self.getValue(element=elemnt, by="CN", by_value='location')
            date_pub = self.getValue(element=elemnt, by="CS", by_value='.time > .date > .date')

            # Methode d'insertion dans la bd
            if titre and image and ville and prix and date_pub:
                self.insertDonnees(titre=titre, image=image, ville=ville, prix=prix, date_pub=date_pub)
                print("Data saved !")
        return

    def insertDonnees(self, image=None, titre=None, prix=None, ville=None, date_pub=None):
        """ En registrement des donnees dans la BD via l'ORM de Django (Model) """
        produit = Produit()
        produit.marque = str(titre).split()[0]
        produit.image = image
        produit.titre = titre
        produit.prix = float("".join(prix.replace('DH', '').split()))
        produit.ville = ville
        produit.date_pub = self.dateParser(date_pub)
        print(produit.date_pub)

        # insertion dans la BD
        try:
            return produit.save()
        except:
            return

    def dateParser(self, datestring):
        if datestring == "Ajourd'hui":
            return datetime.datetime.now()
        elif datestring == "Hier":
            now = datetime.datetime.now()
            return now.date().replace(day=now.date().day - 1)
        else:
            try:
                datestring = datestring.replace("\n", " ").split()
                if len(datestring) < 4:
                    datestring.insert(2, str(datetime.date.today().year))
                datestring = " ".join(datestring)

                date = datetime.datetime.strptime(datestring, '%d %b %Y %I:%M')
                return date
            except:
                return datetime.datetime.now()

    def getValue(self, element, by=None, by_value=""):
        """ methode permettant de recuperer la valeur en text d'un element html sans erreur"""
        try:
            if by == "CN":
                return element.find_element(By.CLASS_NAME, by_value).text
            if by == "CS":
                return element.find_element(By.CSS_SELECTOR, by_value).text
            if by == "TN":
                return element.find_element(By.TAG_NAME, by_value).text

        except NoSuchElementException as ex:
            return ""

    def getAttribut(self, element, by=None, by_value="", attrib=""):
        """ methode permettant de recuperer la valeur en text d'un element html sans erreur"""
        try:
            if by == "CN":
                return element.find_element(By.CLASS_NAME, by_value).get_attribute(attrib)
            if by == "CS":
                return element.find_element(By.CSS_SELECTOR, by_value).get_attribute(attrib)
            if by == "TN":
                return element.find_element(By.TAG_NAME, by_value).get_attribute(attrib)

        except NoSuchElementException as ex:
            return ""






