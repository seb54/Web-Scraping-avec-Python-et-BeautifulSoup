import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import logging
from random import choice

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Liste de User-Agents pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
]

# Initialiser un dictionnaire pour stocker les données récupérées
data = {}

# URL de la première page à scraper
url = "https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=10"

def fetch_page(url, retries=3):
    """Effectue une requête HTTP et gère les erreurs avec des retries."""
    headers = {
        "User-Agent": choice(USER_AGENTS)
    }
    
    for attempt in range(retries):
        try:
            logging.info(f"Requête envoyée à {url}, tentative {attempt + 1}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Si la requête échoue, une exception est levée
            return response.content
        except requests.exceptions.RequestException as e:
            logging.warning(f"Erreur lors de la requête : {e}")
            if attempt < retries - 1:
                logging.info(f"Nouvelle tentative dans 2 secondes...")
                time.sleep(2)
            else:
                logging.error("Échec après plusieurs tentatives.")
                return None

def parse_stock_data(soup):
    """Parse les données des actions"""
    stock_data = {}
    table_rows = soup.find_all('tr', class_='row')

    for row in table_rows:
        cells = row.find_all('td')  # Récupère toutes les cellules <td> dans la ligne
        if len(cells) > 3:  # Vérifie si la ligne a au moins 4 cellules
            symbol = cells[0].text.strip()
            price_raw = cells[1].text.strip()  # Extrait le texte brut de la cellule contenant le prix
            price = price_raw.split(' ')[0]  # Prend uniquement la première partie avant l'espace (le vrai prix)
            change = cells[2].text.strip()
            change_percent = cells[3].text.strip()

            stock_info = {
                "price": price,  # Assigne uniquement le prix
                "change": change,
                "change_percent": change_percent
            }

            # Utiliser le symbole comme clé dans le dictionnaire
            stock_data[symbol] = stock_info
    return stock_data


def save_to_json(data, filename):
    """Sauvegarde les données dans un fichier JSON."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Données exportées avec succès dans {filename}")

def scrape_stocks(url):
    """Scraper les données des actions depuis une URL spécifique."""
    html_content = fetch_page(url)

    if html_content is None:
        logging.error("Impossible de récupérer la page, arrêt du script.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    stock_data = parse_stock_data(soup)

    if stock_data:
        data.update(stock_data)  # Met à jour le dictionnaire avec les nouvelles données
        save_to_json(data, '../data/stock_data.json')

        # Convertir le dictionnaire en DataFrame pandas pour une meilleure lisibilité
        df = pd.DataFrame.from_dict(data, orient='index')
        logging.info("Données scrappées avec succès.")
        print(df)

# Lancer le scraping
scrape_stocks(url)

# Pause pour éviter de surcharger le serveur lors de futures requêtes
time.sleep(2)  # Pause de 2 secondes entre les requêtes si besoin
