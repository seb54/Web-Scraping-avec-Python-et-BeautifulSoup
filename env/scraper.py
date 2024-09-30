import requests # On importe la bibliothèque requests
import sys
from bs4 import BeautifulSoup

# URL de la page à scraper
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# Code ANSI pour le texte en gras et les couleurs
bold_start = "\033[1m"
bold_end = "\033[0m"
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
cyan = "\033[96m"
gray = "\033[90m"

reset = "\033[0m"  # Réinitialise les styles

# Trouver toutes les div ayant la classe "card-content"
try:
    results = soup.find_all(class_="card-contente")
    if len(results) == 0:  # Vérifier si la liste des offres est vide
        raise ValueError("Aucune offre d'emploi n'a pu être récupérée car aucune div ayant la classe 'card-content' n'a été trouvée")
except ValueError as e:
    print(f"{red}Erreur : {e}{reset}")
    print("Fin du programme")
    sys.exit(1)  # Ferme le programme en cas d'erreur

# Titre principal avec couleur
print(f"{cyan}Liste des offres d'emploi sur la page {URL}{reset}\n")

# Pour chaque div "card-content", chercher le h2 avec la classe "title"

for result in results:
    try:
        job_title = result.find("h2", class_="title")
        if job_title is None:
            raise ValueError("Aucune offre d'emploi trouvée. Vérifie qu'il y a bien un titre H2 ayant la classe 'title'")
        
        job_company = result.find("h3", class_="subtitle")
        if job_company is None:
            raise ValueError(f"Aucun nom de société trouvé pour l'offre {job_title.text}. Vérifie qu'il y a bien un titre H3 ayant la classe 'subtitle'")
        
        job_location = result.find("p", class_="location")
        if job_location is None:
            raise ValueError(f"Aucune donnée de localisation trouvée pour l'offre {job_title.text}. Vérifie s'il y a bien un paragraphe ayant la classe 'location'")
        
        job_datetime = result.find("time")
        if job_datetime is None:
            raise ValueError(f"Aucune date trouvée pour l'offre {job_title.text}. Vérifie s'il y a bien une balise <time>")
        
        # Afficher les informations avec des couleurs
        print(f"{bold_start}{blue}Titre du job : {reset}{bold_start}{job_title.text.strip()}{bold_end}")
        print(f"{green}Société : {reset}{job_company.text.strip()}")
        print(f"{yellow}Localisation : {reset}{job_location.text.strip()}")
        print(f"{gray}Date de publication : {reset}{job_datetime.text.strip()}\n")

    except ValueError as e:
        print(f"{red}Erreur : {e}{reset}")
        print("Fin du programme")
        sys.exit(1)  # Ferme le programme en cas d'erreur
