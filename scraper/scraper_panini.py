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
output_file = "marvel_panini_data.json"

# Vérification et initialisation de la structure du fichier JSON
if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            output = json.load(f)
    except json.JSONDecodeError:
        print("[Erreur] Le fichier JSON est corrompu. Initialisation avec des données vides.")
        output = {"Comics": {"Marvel": []}}
else:
    print("[Info] Fichier JSON non trouvé ou vide. Initialisation avec des données vides.")
    output = {"Comics": {"Marvel": []}}

# Configuration Selenium
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def normalize_text(text):
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

def clean_title(raw_title):
    return raw_title.replace("Panini: Comics_", "").strip()

def scrape_page(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-image-photo"))
        )
    except Exception as e:
        print(f"[Erreur] Chargement de la page : {e}")
        return

    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    comics_elements = soup.find_all("img", {"class": "product-image-photo", "alt": True, "src": True})

    if not comics_elements:
        print("[Info] Aucun élément image trouvé.")
        return

    print(f"✔️ {len(comics_elements)} éléments détectés.")
    existing_titles = {comic["title"] for comic in output["Comics"]["Marvel"]}

    for img in comics_elements:
        try:
            raw_title = img.get("alt").strip()
            title = normalize_text(clean_title(raw_title))
            img_url = img.get("src").strip()

            print(f"Titre: {title}, URL: {img_url}")

            if "data:image/" in img_url or not is_valid_url(img_url):
                print("[Info] Image non valide ou encodée en base64, ignorée.")
                continue

            if not title or title in existing_titles:
                print(f"[Info] Comic ignoré (vide ou doublon): {title}")
                continue

            output["Comics"]["Marvel"].append({
                "title": title,
                "poster": img_url
            })
            existing_titles.add(title)
            print(f"✅ Ajouté: {title}")
        except Exception as e:
            print(f"[Erreur] Problème avec un comic : {e}")

def scrape_all_pages(base_url, total_pages):
    for page_num in range(1, total_pages + 1):
        page_url = f"{base_url}?p={page_num}"
        print(f"\n--- Scraping page {page_num} ---")
        scrape_page(page_url)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"✅ Données sauvegardées dans {output_file}")

# URL de base et nombre de pages à scraper
base_url = "https://www.panini.fr/shp_fra_fr/comics-mangas-magazines/marvel.html"
total_pages = 117  # À ajuster selon le nombre de pages à scraper

scrape_all_pages(base_url, total_pages)
driver.quit()
