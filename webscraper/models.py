import csv, json
from django.core.serializers import serialize
from django.db import models, connection

# Create your models here.

class Produit(models.Model):
    """ La classe des produits """
    marque = models.CharField(verbose_name="Marque", max_length=300, blank=True, null=True)  # marque du produit
    image = models.CharField(max_length=300, blank=True, null=True)     # url image du produit
    titre = models.CharField(max_length=300, blank=True, null=True, unique=True)    # le titre du produit
    prix = models.FloatField(blank=True, null=True)     # le prix du produit
    ville = models.CharField(max_length=100, blank=True, null=True)    # la ville du produit
    date_pub = models.DateTimeField(verbose_name="Date  de publication", null=True)   # la date et l'heure du produit

    def __str__(self):
        return self.titre

    def enregistre_to_DB(self):
        return self.save()

    def get_all_Json(self):
        produits_json = {"data": []}
        for d in json.loads(serialize("json", Produit.objects.all().order_by("id"))):
            d["fields"]["id"] = d["pk"]
            produits_json["data"].append(d["fields"])

        produits_json['recordsTotal'] = len(produits_json["data"])
        produits_json['recordsFiltered'] = len(produits_json["data"])
        return json.dumps(produits_json)

    def get_moyenne_to_json(self):
        produits = list()
        with connection.cursor() as cursor:
            req_sql = f"select marque, ville, avg(prix) as prixmoyen from {Produit._meta.db_table} group by ville, marque"
            cursor.execute(req_sql)
            produits = cursor.fetchall()

        produits_dic = {
            'data': [],
        }
        for p in produits:
            produits_dic["data"].append({
                "marque": p[0],
                "ville": p[1],
                "prixmoyen": p[2]
            })
        produits_dic['recordsTotal'] = len(produits_dic["data"])
        produits_dic['recordsFiltered'] = len(produits_dic["data"])
        return json.dumps(produits_dic)

    def write_to_csv(self, response):
        writer = csv.writer(response)
        writer.writerow(['ID', 'MARQUE', 'TITRE', 'PRIX', 'VILLE', 'DATE'])

        values_list = "id", "marque", "titre", "prix", "ville", "date_pub"
        for element in Produit.objects.all().values_list(values_list):
            writer.writerow(element)

        response['Content-Disposition'] = 'attachment; filename="liste_des_produits.csv"'
        return response
