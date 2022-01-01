from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db import connection
from django.template.loader import render_to_string
import csv, json
from ..scraperthreading.scraperthread import scraperthreadRunner
from ..models import Produit
from ..formulaire import FormulaireSaisie


# Create your views here.
def pageAccueil(request):
    scraperthreadRunner()
    return render(request, 'accueil.html')


def pageMoyennePrix(request):
    return render(request, 'moyenneprix.html')


def pageRecherche(request):
    formulaire = FormulaireSaisie()
    return render(request, 'formulaire.html', {"formulaire" : formulaire})


def getDonnesFromBD(request):
    produits = Produit.objects.all().order_by("id")
    produits_json = serialize("json", produits)
    return HttpResponse(produits_json, content_type="application/json")

def getMoyennePrix(request):
    with connection.cursor() as cursor:
        cursor.execute(f"select marque, ville, avg(prix) as prixmoyen from {Produit._meta.db_table} group by ville, marque")
        produit = cursor.fetchall()

    dic = dict()
    dic["produits"] = []
    for p in produit:
        dic["produits"].append({
            "marque" : p[0],
            "ville" : p[1],
            "prixmoyen" : p[2]
        })
    return HttpResponse(json.dumps(dic["produits"]), content_type="application/json")


def envoiMail(request):
    if request.method == "POST":
        email = request.POST.get("email")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
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
        messages.SUCCESS(request, "Email bien envoyé !")
        return redirect("webscraper:pageRecherche")
    else:
        messages.ERROR(request, "Veuillez reésayer !")
        return redirect("webscraper:pageRecherche")

def renderTocsv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['ID', 'MARQUE', 'TITRE', 'PRIX', 'VILLE', 'DATE'])

    for element in Produit.objects.all().values_list("id", "marque", "titre", "prix", "ville", "date_pub"):
        writer.writerow(element)

    response['Content-Disposition'] = 'attachment; filename="liste_des_produits.csv"'
    return response

