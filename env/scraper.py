import requests # On importe la bibliothèque requests
import sys
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# Code ANSI pour le texte en gras
bold_start = "\033[1m"
bold_end = "\033[0m"

# Trouver toutes les div ayant la classe "card-content"
results = soup.find_all(class_="card-content")

# Pour chaque div "card-content", chercher le h2 avec la classe "title"

print("Liste des offres d'emploi sur la page https://realpython.github.io/fake-jobs/")
for result in results:
    try:
        job_title = result.find("h2", class_="title")
        if job_title is None:
            raise ValueError("Aucun job trouvé avec un titre H2 ayant la classe 'title'. FIN")
        
        job_company = result.find("h3", class_="subtitle")
        if job_company is None:
            raise ValueError(f"Aucun nom de société avec titre H3 ayant la classe 'subtitle' trouvé pour l'offre {job_title.text}")
        
        job_location = result.find("p", class_="location")
        if job_location is None:
            raise ValueError(f"Aucune donnée de localisation trouvée pour l'offre {job_title.text}")

        # Pour chaque h2 trouvé, l'afficher avec une ligne de séparation
        print(bold_start + "Titre du job : " + job_title.text + bold_end, end="\n")
        print ("Société : " + job_company.text, end="\n")
        print ("Localisation : " + job_location.text.strip(), end="\n"*2)

    except ValueError as e:
        print(f"Erreur : {e}")
        print("Fin du programme")
        sys.exit(1)  # Ferme le programme en cas d'erreur
