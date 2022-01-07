from django import forms
from .models import Produit

class FormulaireSaisie(forms.Form):
    liste_produits = []
    for p in Produit.objects.all().values("ville").distinct().order_by("ville"):
        liste_produits.append((p["ville"], p["ville"]))

    ville = forms.ChoiceField(choices=liste_produits)
    prix_min = forms.IntegerField(label='Prix minimum')
    prix_max = forms.IntegerField(label='Prix maximum')
    date_debut = forms.DateField(label='Date de debut', input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'datetimepicker1'
        }))
    date_fin = forms.DateField(label='Date de fin', input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'datetimepicker2'
        }))
    email = forms.EmailField(label='Adresse email')

