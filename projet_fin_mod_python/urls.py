from django.urls import path, include

urlpatterns = [
    path("", include("webscraper.urls"))    # Inclusion des urls de l'application webscraper
]
