from django.urls import path
from .vues.views import pageAccueil, getMoyennePrix, getDonnesFromBD, renderTocsv, envoiMail

app_name = "webscraper"
urlpatterns = [
    path("", pageAccueil, name="pageAccueil"),
    path("get_moyenne_prix", getMoyennePrix, name="getMoyennePrix"),
    path("get_donnes_from_bd", getDonnesFromBD, name="getDonnesFromBD"),
    path("render_to_csv", renderTocsv, name="renderTocsv"),
    path("envoi_email", envoiMail, name="envoiMail"),
]