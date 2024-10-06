import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import logging
from random import choice
from typing import Optional

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
URL = "https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=10"

def fetch_page(url: str, retries: int = 3) -> Optional[BeautifulSoup]:
    """Effectue une requête HTTP et gère les erreurs avec des retries."""
    headers = {
        "User-Agent": choice(USER_AGENTS)
    }
    
    for attempt in range(retries):
        try:
            logging.info(f"Requête envoyée à {url}, tentative {attempt + 1}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logging.warning(f"Erreur lors de la requête : {e}")
            if attempt < retries - 1:
                logging.info("Nouvelle tentative dans 2 secondes...")
                time.sleep(2)
            else:
                logging.error("Échec après plusieurs tentatives.")
                return None

def parse_stock_data(soup: BeautifulSoup) -> dict:
    """Parse les données des actions"""
    stock_data = {}
    table_rows = soup.find_all('tr', class_='row')

    for row in table_rows:
        cells = row.find_all('td')
        if len(cells) > 3:
            symbol = cells[0].text.strip()
            price = cells[1].text.strip().split(' ')[0]
            change = cells[2].text.strip()
            change_percent = cells[3].text.strip()

            stock_info = {
                "price": price,
                "change": change,
                "change_percent": change_percent
            }

            stock_data[symbol] = stock_info
    return stock_data

def save_to_json(data: dict, filename: str):
    """Sauvegarde les données dans un fichier JSON."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    logging.info(f"Données exportées avec succès dans {filename}")

def scrape_stocks(url: str):
    """Scraper les données des actions depuis une URL spécifique."""
    soup = fetch_page(url)
    if not soup:
        logging.error("Impossible de récupérer la page, arrêt du script.")
        return

    stock_data = parse_stock_data(soup)
    if stock_data:
        data.update(stock_data)
        save_to_json(data, '../data/stock_data.json')

        df = pd.DataFrame.from_dict(data, orient='index')
        logging.info("Données scrappées avec succès.")
        print(df)

def main():
    scrape_stocks(URL)
    time.sleep(2)

if __name__ == "__main__":
    main()