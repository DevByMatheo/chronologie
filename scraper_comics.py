import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Fichier de sortie JSON
output_file = "comics_data.json"

# Vérification et initialisation de la structure du fichier JSON
if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            output = json.load(f)
    except json.JSONDecodeError:
        print("[Erreur] Le fichier JSON est corrompu. Initialisation avec des données vides.")
        output = {"Comics": {"Canon": []}}
else:
    print("[Info] Fichier JSON non trouvé ou vide. Initialisation avec des données vides.")
    output = {"Comics": {"Canon": []}}

# Configurer Selenium et ChromeDriver
options = Options()
options.add_argument("--headless")  # Pour exécuter le navigateur en mode sans tête
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fonction de nettoyage du texte (enlève les accents et convertit en minuscules)
def normalize_text(text):
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Fonction de validation de l'URL (vérifie si elle commence par http ou https)
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Fonction de scraping de la page
def scrape_page(url):
    driver.get(url)

    # Attendre que les images de comics soient présentes
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
    except Exception as e:
        print(f"[Erreur] Problème de chargement de la page : {e}")
        return

    time.sleep(3)  # Attendre un peu après le chargement complet pour plus de fiabilité

    # Extraire le contenu HTML de la page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Sélectionner tous les éléments de comics (les images de couverture)
    comics_elements = soup.find_all("img", {"alt": True, "src": True})

    if not comics_elements:
        print("[Erreur] Aucun élément d'image trouvé.")
        return

    print(f"Trouvé {len(comics_elements)} éléments de comics.")
    
    # Créer un set pour éviter les doublons
    existing_titles = {comic["title"] for comic in output["Comics"]["Canon"]}

    for img in comics_elements:
        try:
            title = normalize_text(img.get("alt").strip())  # Normalisation du titre
            img_url = img.get("src").strip()  # Extraire l'URL de l'image

            # Afficher le titre et l'URL pour déboguer
            print(f"Titre: {title}, URL: {img_url}")

            # Si l'URL est une base64 ou vide, ignorer cette image
            if "data:image/" in img_url or not img_url:
                img_url = "Poster non disponible"
            
            # Validation de l'URL
            if not is_valid_url(img_url):
                img_url = "Poster non disponible"

            # Si l'URL est de type "Poster non disponible", l'ignorer
            if img_url == "Poster non disponible" or not title:
                print(f"[Info] Ignoré le comic avec titre '{title}' et URL '{img_url}'.")
                continue

            # Ajouter le comic s'il n'est pas déjà dans le fichier JSON
            if title in existing_titles:
                print(f"[Info] Doublon trouvé pour '{title}', passage.")
                continue

            output["Comics"]["Canon"].append({
                "title": title,
                "poster": img_url
            })
            existing_titles.add(title)  # Ajouter le titre au set des titres traités
            print(f"✅ {title}")
        except Exception as e:
            print(f"[Erreur] Problème avec le comic '{title}' (URL: {img_url}): {e}")

# Fonction pour naviguer à travers les pages
def scrape_all_pages(base_url, total_pages):
    for page_num in range(1, total_pages + 1):
        page_url = f"{base_url}?page={page_num}"
        print(f"\nScraping de la page {page_num} : {page_url}")
        scrape_page(page_url)

    # Sauvegarder les données dans le fichier JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"Fichier JSON mis à jour : {output_file}")

# URL de la première page à scraper
base_url = "https://www.senscritique.com/liste/star_wars_integrale_chronologique_de_l_univers_etendu_canon/1619248"
total_pages = 5  # Nombre de pages à scraper

# Scraper toutes les pages
scrape_all_pages(base_url, total_pages)

# Fermer le navigateur Selenium après le scraping
driver.quit()
