import requests # On importe la bibliothèque requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# On affiche tout le code HTML de la page
print(page.text)

# On met le contenu de la div ResultsContainer dans la variable results
# results = soup.find(class_="title")

job_title =  soup.find(class_="title")
for job_element in job_title:
    print(job_element, end="\n"*2)
print(job_title.prettify())
