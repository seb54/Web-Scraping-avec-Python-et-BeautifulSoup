import requests # On importe la bibliothèque requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# On affiche tout le code HTML de la page
print(page.text)

# On met le contenu de la div ResultsContainer dans la variable results
results = soup.find(class_="title")
print(results.prettify())
