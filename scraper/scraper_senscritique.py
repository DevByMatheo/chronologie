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
options.add_argument("--headless")  # Mode sans tête
options.add_argument("--window-size=1920,1080")  # S'assurer que les lazy-load se déclenchent
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fonction de nettoyage du texte
def normalize_text(text):
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).strip().lower()

# Fonction de validation de l'URL
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Fonction de scraping d'une page
def scrape_page(url):
    driver.get(url)

    # Scroller pour forcer le lazy-load des images
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    comics_elements = soup.find_all("img", {"alt": True})

    if not comics_elements:
        print("[Erreur] Aucun élément d'image trouvé.")
        return

    print(f"Trouvé {len(comics_elements)} éléments de comics.")
    existing_titles = {comic["title"] for comic in output["Comics"]["Canon"]}

    for img in comics_elements:
        try:
            title = normalize_text(img.get("alt", ""))
            # Récupérer l'image réelle (lazy-load)
            img_url = img.get("src") or img.get("data-src") or img.get("data-lazy") or ""
            
            if "data:image/" in img_url or not is_valid_url(img_url):
                img_url = "Poster non disponible"

            if not title or img_url == "Poster non disponible":
                print(f"[Info] Ignoré le comic avec titre '{title}' et URL '{img_url}'.")
                continue

            if title in existing_titles:
                print(f"[Info] Doublon trouvé pour '{title}', passage.")
                continue

            output["Comics"]["Canon"].append({
                "title": title,
                "poster": img_url
            })
            existing_titles.add(title)
            print(f"✅ {title} -> {img_url}")
        except Exception as e:
            print(f"[Erreur] Problème avec le comic '{title}' : {e}")

# Fonction pour naviguer toutes les pages
def scrape_all_pages(base_url, total_pages):
    for page_num in range(1, total_pages + 1):
        page_url = f"{base_url}?page={page_num}"
        print(f"\nScraping de la page {page_num} : {page_url}")
        scrape_page(page_url)

    # Sauvegarder dans le JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    print(f"Fichier JSON mis à jour : {output_file}")

# URL et nombre de pages
base_url = "https://www.senscritique.com/liste/dc_animated_universe_ordre_de_visionnage/609146"
total_pages = 2

scrape_all_pages(base_url, total_pages)
driver.quit()
