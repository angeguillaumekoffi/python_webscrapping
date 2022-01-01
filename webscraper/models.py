from django.db import models

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



