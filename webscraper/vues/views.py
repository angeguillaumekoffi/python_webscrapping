from datetime import datetime
from django.conf.global_settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from ..scraperthreading.scraperthread import scraperthreadRunner
from ..models import Produit
from ..formulaire import FormulaireSaisie


# Create your views here.
def pageAccueil(request):
    """ Vue qui renvoi la page d'accueil en html"""
    scraperthreadRunner()
    print("EMAIL_HOST_USER : ", EMAIL_HOST_USER)
    print("EMAIL_HOST_PASSWORD : ", EMAIL_HOST_PASSWORD)
    return render(request, 'accueil.html')


def pageMoyennePrix(request):
    """ Vue qui renvoi la page de la moyenne des prix en html"""
    return render(request, 'moyenneprix.html')


def pageRecherche(request):
    """ Vue qui renvoi la page de recherche en html"""

    formulaire = FormulaireSaisie()
    return render(request, 'formulaire.html', {"formulaire" : formulaire})


def getDonnesFromBD(request):
    """ Vue qui renvoi les données en format json"""
    produits_json = Produit().get_all_Json()
    return HttpResponse(produits_json, content_type="application/json")


def getMoyennePrix(request):
    """ Vue qui renvoi la moyenne des prix en format json"""
    produits_json = Produit().get_moyenne_to_json()
    return HttpResponse(produits_json, content_type="application/json")


def renderTocsv(request):
    """ Vue qui renvoi les donnees en format csv"""
    response = HttpResponse(content_type='text/csv')
    return Produit().write_to_csv(response=response)


def envoiMail(request):
    """ Vue qui recherche les produit du filtre et envoi le mail"""
    if request.method == "POST":
        email = request.POST.get("email")
        date_debut = datetime.strptime(request.POST.get("date_debut"), '%d/%m/%Y')
        date_fin = datetime.strptime(request.POST.get("date_fin"), '%d/%m/%Y')
        prix_min = request.POST.get("prix_min")
        prix_max = request.POST.get("prix_max")
        ville = request.POST.get("ville")

        liste_produits = Produit.objects.filter(prix__gte=prix_min, prix__lte=prix_max, date_pub__gte=date_debut, date_pub__lte=date_fin, ville=ville)

        html_message = render_to_string('html_email_body.html', {'liste_produits': liste_produits})
        send_mail(
            subject='Produits from scraper',
            message="",
            html_message=html_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[str(email)],
            fail_silently=False,
        )
        messages.success(request, "Email bien envoyé !")
        return redirect("webscraper:pageRecherche")
    else:
        messages.error(request, "Veuillez reésayer !")
        return redirect("webscraper:pageRecherche")