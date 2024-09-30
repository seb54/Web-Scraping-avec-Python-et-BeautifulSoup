import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# Initialiser une liste pour stocker les données récupérées
data = []

# URL de la première page à scraper
url = "https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=10"

# Effectuer la requête HTTP pour récupérer le contenu de la page
response = requests.get(url)
if response.status_code != 200:
    print(f"Erreur lors de la requête HTTP : {response.status_code}")
    exit()

# Utiliser BeautifulSoup pour parser le contenu HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Récupérer toutes les lignes du tableau contenant les informations sur les actions
table_rows = soup.find_all('tr', class_='row')


# Parcourir chaque ligne et récupérer les informations souhaitées
for row in table_rows:
    cells = row.find_all('td')  # Récupère toutes les cellules <td> dans la ligne
    if len(cells) > 3:  # Vérifie si la ligne a au moins 4 cellules
        symbol = cells[0].text.strip()  # Première colonne : symbole
        price = cells[1].text.strip()   # Deuxième colonne : prix
        change = cells[2].text.strip()  # Troisième colonne : changement
        change_percent = cells[3].text.strip()  # Quatrième colonne : pourcentage de changement

        # Fais ce que tu veux avec ces valeurs (les stocker, afficher, etc.)
        print(f"Symbol: {symbol}, Price: {price}, Change: {change}, Change Percent: {change_percent}")


        # Ajouter les informations dans une structure de dictionnaire
        stock_info = {
            "symbol": symbol,
            "price": price,
            "change": change,
            "change_percent": change_percent
        }

        # Ajouter ce dictionnaire à la liste 'data'
        data.append(stock_info)

# Exporter les données en format JSON
with open('stock_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Les données ont été exportées avec succès dans 'stock_data.json'")

# Convertir la liste en DataFrame pandas pour une meilleure lisibilité
df = pd.DataFrame(data)

# Afficher les résultats
print(df)
