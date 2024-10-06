import requests
import sys
from bs4 import BeautifulSoup
from typing import Optional

# URL de la page à scraper
URL = "https://realpython.github.io/fake-jobs/"
ANSI_CODES = {
    "bold_start": "\033[1m",
    "bold_end": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "gray": "\033[90m",
    "reset": "\033[0m"
}


def fetch_page_content(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"{ANSI_CODES['red']}Erreur lors de la requête : {e}{ANSI_CODES['reset']}")
        return None


def scrape_jobs(soup: BeautifulSoup):
    results = soup.find_all(class_="card-content")
    if len(results) == 0:
        handle_error("Aucune offre d'emploi n'a pu être récupérée car aucune div ayant la classe 'card-content' n'a été trouvée")
    return results


def extract_job_data(result) -> dict:
    job_data = {}
    job_data['title'] = get_element_text(result, "h2", "title", "Aucune offre d'emploi trouvée. Vérifie qu'il y a bien un titre H2 ayant la classe 'title'")
    job_data['company'] = get_element_text(result, "h3", "subtitle", f"Aucun nom de société trouvé pour l'offre {job_data['title']}")
    job_data['location'] = get_element_text(result, "p", "location", f"Aucune donnée de localisation trouvée pour l'offre {job_data['title']}")
    job_data['datetime'] = get_element_text(result, "time", None, f"Aucune date trouvée pour l'offre {job_data['title']}")
    job_apply_element = result.find("a", string=lambda text: "Apply" in text)
    if not job_apply_element:
        handle_error(f"Aucun lien trouvé pour postuler à l'offre {job_data['title']}")
    job_data['apply_link'] = job_apply_element.get('href')
    job_data['description'] = get_job_description(job_data['apply_link'])
    return job_data


def get_element_text(result, tag: str, class_name: Optional[str], error_message: str) -> str:
    element = result.find(tag, class_=class_name) if class_name else result.find(tag)
    if not element:
        handle_error(error_message)
    return element.text.strip()


def get_job_description(url: str) -> str:
    soup = fetch_page_content(url)
    if not soup:
        handle_error("Impossible de récupérer la description de l'offre")
    result_description = soup.find("div", class_="content")
    job_description = result_description.find("p") if result_description else None
    return job_description.text.strip() if job_description else "Non disponible"


def handle_error(message: str):
    print(f"{ANSI_CODES['red']}Erreur : {message}{ANSI_CODES['reset']}")
    sys.exit(1)


def display_job_info(job_data: dict):
    print(f"{ANSI_CODES['bold_start']}{ANSI_CODES['blue']}Titre du job : {ANSI_CODES['reset']}{job_data['title']}{ANSI_CODES['bold_end']}")
    print(f"{ANSI_CODES['green']}Société : {ANSI_CODES['reset']}{job_data['company']}")
    print(f"{ANSI_CODES['yellow']}Localisation : {ANSI_CODES['reset']}{job_data['location']}")
    print(f"{ANSI_CODES['blue']} Description de l'offre : {ANSI_CODES['reset']}{job_data['description']}")
    print(f"{ANSI_CODES['gray']}Date de publication : {ANSI_CODES['reset']}{job_data['datetime']}")
    print(f"Postuler ici : {ANSI_CODES['blue']}{job_data['apply_link']}{ANSI_CODES['reset']}\n")


def main():
    soup = fetch_page_content(URL)
    if not soup:
        handle_error("Impossible de récupérer la page principale des offres d'emploi")

    job_results = scrape_jobs(soup)
    print(f"{ANSI_CODES['cyan']}Liste des offres d'emploi sur la page {URL}{ANSI_CODES['reset']}\n")

    for result in job_results:
        job_data = extract_job_data(result)
        display_job_info(job_data)

    print(f"Nombre d'offres trouvées et affichées : {len(job_results)}")


if __name__ == "__main__":
    main()