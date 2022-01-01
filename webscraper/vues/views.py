from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db import connection
from django.template.loader import render_to_string
import csv, json
from ..scraperthreading.scraperthread import scraperthreadRunner
from ..models import Produit


# Create your views here.
def pageAccueil(request):
    scraperthreadRunner()
    return render(request, 'index.html')

def getDonnesFromBD(request):
    produits = Produit.objects.all().order_by("-date_pub")
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
        print(serialize("json", liste_produits))

        html_message = render_to_string('html_email_body.html', {'liste_produits': liste_produits})
        send_mail(
            subject='Produits from scraper',
            message="",
            html_message=html_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[str(email)],
            fail_silently=False,
        )
        message = "Email bien envoyé !"
        return HttpResponse({"status": "ok", "message":str(message)})

def renderTocsv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['ID', 'MARQUE', 'TITRE', 'PRIX', 'VILLE', 'DATE'])

    for element in Produit.objects.all().values_list("id", "marque", "titre", "prix", "ville", "date_pub"):
        writer.writerow(element)

    response['Content-Disposition'] = 'attachment; filename="liste_des_produits.csv"'

    return response

