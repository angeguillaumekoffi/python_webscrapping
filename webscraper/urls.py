from django.urls import path
from .vues.views import pageAccueil, pageRecherche, pageMoyennePrix, getMoyennePrix, getDonnesFromBD, renderTocsv, envoiMail

app_name = "webscraper"
urlpatterns = [
    path("", pageAccueil, name="pageAccueil"),
    path("page_de_echerche", pageRecherche, name="pageRecherche"),
    path("page_moyenne_des_prix", pageMoyennePrix, name="pageMoyennePrix"),
    path("get_moyenne_prix", getMoyennePrix, name="getMoyennePrix"),
    path("get_donnes_from_bd", getDonnesFromBD, name="getDonnesFromBD"),
    path("render_to_csv", renderTocsv, name="renderTocsv"),
    path("envoi_email", envoiMail, name="envoiMail"),
]