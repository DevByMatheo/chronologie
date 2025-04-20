import requests
import json

API_KEY = "ebbcc734fc96cfc0930e5635cf9c5c65"
SEARCH_URL = "https://api.themoviedb.org/3/search/multi"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

titles = [
        "Ant-Man et la Guêpe Quantumania",
        "Les Gardiens de la Galaxy 3",
        "Wonder Man",
        "Secret Invasion Saison 1",
        "Spider-Man 4",
        "The Marvels",
        "Armor Wars",
        "Loki Saison 2",
        "What If Et si… le Strange Suprême était intervenu ?",
        "What If Et si.. Saison 3 Episode 8",
        "Deadpool et Wolverine",
        "Marvel Zombies",
        "Captain AmericaBrave New World",
        "Thunderbolts",
        "The Fantastic Four",
        "Avengers The Kang Dynasty",
        "Avengers Secret Wars",
]

phases = {
    "1941-1945": [],
    "1946-1947": [],
    "1962-2002": [],
    "2002-2006": [],
    "2007-2010": [],
    "2010-2012": [],
    "Phase 2": [],
    "Phase 3": [],
    "Phase 4": [],
    "Phase 5": [],
    "1941 -1945": [],
    "1946 -1947": [],
    "1962 -2002": [],
    "2002 -2006": [],
    "2007 -2010": [],
    "2010 -2012": [],
    "2013 -2016": [],
    "2016-2017": [],
    '2017 -2022': [],
    "2024-2025": [],
    "2024-2026": [],
    "2025": [],
    "2026": [],
    "2023": [],
    "Inconnue": [] 
}



def get_poster(title):
    params = {
        "api_key": API_KEY,
        "query": title
    }
    
    response = requests.get(SEARCH_URL, params=params)
    
    if response.status_code != 200:
        print(f"⚠️ Erreur pour {title} : Status {response.status_code}")
        return None
    
    data = response.json()
    
    if "results" in data and data["results"]:
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return IMAGE_BASE + poster_path
    return None


def determine_phase(title):
    phase_mapping = {
   # Phase 6 : 2010 - 2012
        "Iron Man": "2010 -2012",
        "What If Et si… Killmonger avait sauvé Tony Stark ?": "2010 -2012",
        "Iron Man 2": "2010 -2012",
        "What If Et si… Le monde avait perdu ses plus puissants héros ?": "2010 -2012",
        "Thor": "2010 -2012",
        "What If Et si… Thor avait été fils unique ?": "2010 -2012",
        "L’incroyable Hulk": "2010 -2012",
        "What If Et si...Kahhori avait refait le monde ?": "2010 -2012",
        "What If Et si.. Saison 3 Episode 1": "2010 -2012",
        "One Shot : Le Consultant": "2010 -2012",
        "One Shot : Une Drôle d'Histoire en Allant Voir le Marteau de Thor": "2010 -2012",
        "Ghost Rider Spirit of Vengeance": "2010 -2012",
        "Avenger": "2010 -2012",
        "What If Et si... Iron Man avait rencontré le Grand Maître ?": "2010 -2012",
        "One Shot : Objet 47": "2010 -2012",
        "Iron Man 3": "2010 -2012",

        # Phase 2 : 2013 - 2016
        "Wolverine : Le Combat de l’Immortel": "2013 -2016",
        "One Shot : Longue Vie au Roi": "2013 -2016",
        "The Amazing Spider-Man": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 1 - Épisodes 1 à 7": "2013 -2016",
        "The Amazing Spider-Man : le Destin d’un Héros": "2013 -2016",
        "Thor : le Monde des Ténèbres": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 1 - Épisodes 8 à 16": "2013 -2016",
        "What If Et si... Happy Hogan avait sauvé Noël ?": "2013 -2016",
        "Captain America : Le Soldat de l’Hiver": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 1 - Épisodes 17 à 22": "2013 -2016",
        "Les Gardiens de la Galaxie": "2013 -2016",
        "What If Et si... Nebula avait rejoint les cohortes de Nova ?": "2013 -2016",
        "Les Gardiens de la Galaxie Vol. 2": "2013 -2016",
        "What If Et si.. Saison 3 Episode 4": "2013 -2016",
        "What If Et si… Peter Quill avait attaqué les plus grands héros de la Terre ?": "2013 -2016",
        "Je S’appelle Groot Saison 1 & 2": "2013 -2016",
        "Daredevil Saison 1": "2013 -2016",
        "Jessica Jones Saison 1": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 2 - Épisodes 1 à 19": "2013 -2016",
        "What If Et si… Le Gardien avait rompu son serment ?": "2013 -2016",
        "Avengers : L’Ère d’Ultron": "2013 -2016",
        "What If Et si… Ultron avait gagné ?": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 2 - Épisodes 20 à 22": "2013 -2016",
        "WHiH Newsfront Saison 1 - Webisodes 1 à 5": "2013 -2016",
        "Ant-Man": "2013 -2016",
        "Spider-Man : Freshman Year Saison 1": "2013 -2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 3 - Épisodes 1 à 19": "2013 -2016",
        "Spider-Man : Sophomore Year Saison 2": "2013 -2016",

        # Phase 3 : 2016
        "WHiH Newsfront Saison 1 - Webisodes 6 à 10": "2016",
        "Daredevil Saison 2": "2016",
        "Luke Cage Saison 1": "2016",
        "Iron Fist Saison 1": "2016",
        "The Defenders Saison 1": "2016",
        "Cloak and Dagger Saison 1": "2016",
        "WHiH Newsfront Saison 2": "2016",
        "Captain America Civil Wars": "2016",
        "One shot Team Thor 1": "2016",
        "A Film by Peter Parker": "2016",
        "Black Widow": "2016",
        "Black Panther": "2016",
        "What If Et si… T’Challa était devenu Star Lord": "2016",
        "Spider-Man Homecoming": "2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 3 - Épisodes 20 à 22": "2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 4 - Épisodes 1 à 8": "2016",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 4 - Épisodes 9 à 22": "2016",
        "The Punisher Saison 1": "2016",
        "Deadpool": "2016",
        "Deadpool 2": "2016",
        "Les Nouveaux Mutants": "2016",
        "Logan": "2016",
        "Doctor Strange": "2016",
        "What If Et si… Doctor Strange avait perdu son coeur au lieu de ses mains ?": "2016",
        "The Gifted Saison 1": "2016",

        # Phase 4 : 2017 - 2022
        "One shot Team Thor 2": "2017 -2022",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 5 - Épisodes 1 à 18": "2017 -2022",
        "Inhumans Saison 1": "2017 -2022",
        "Jessica Jones Saison 2": "2017 -2022",
        "Luke Cage Saison 2": "2017 -2022",
        "Iron Fist Saison 2": "2017 -2022",
        "Daredevil Saison 3": "2017 -2022",
        "Cloak Dagger Saison 2": "2017 -2022",
        "Thor Ragnarok": "2017 -2022",
        "Team Darryl": "2017 -2022",
        "The Gifted Saison 2": "2017 -2022",
        "The Punisher Saison 2": "2017 -2022",
        "Jessica Jones Saison 3": "2017 -2022",
        "Runaways Saison 3 Episode 1 à 9": "2017 -2022",
        "Ant-Man et la Guêpe": "2017 -2022",
        "Avengers Infinity War": "2017 -2022",
        "What If Et si… Les Avengers se rassemblent en 1602 ?": "2017 -2022",
        "What If Et si.. Saison 3 Episode 6": "2017 -2022",
        "What If Et si…Saison 1 episode 5": "2017 -2022",
        "What If Et si.. Saison 3 Episode 7": "2017 -2022",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 5 - Épisodes 19 à 22": "2017 -2022",
        "Venom": "2017 -2022",
        "Marvel : Les Agents du S.H.I.E.L.D. Saison 6 & 7": "2017 -2022",
        "Helstrom Saison 1": "2017 -2022",
        "Runaways Saison 3 Episode 10": "2017 -2022",
        "Avengers Endgame": "2023",

        # Phase 5 : 2023-2026

        "Loki Saison 1": "2024-2025",
        "Wanda Vision Saison 1": "2024-2025",
        "Spider-Man into the Spider-Verse": "2024-2025",
        "Spider-ham caught in a ham": "2024-2025",
        "Légion Saison 1 & 2 & 3": "2024-2025",
        "Le Faucon et le Soldat de l’Hiver Saison 1": "2024-2025",
        "Shang-Chi et la légende des Dix Anneaux": "2024-2025",
        "What If Saison 2 Episode 7": "2024-2025",
        "The Daily Bugle Saison 1": "2024-2025",
        "Les Eternels": "2024-2025",
        "What If Et si.. Saison 3 Episode 5": "2024-2025",
        "La liste des courses de Peter": "2024-2025",
        "Marvel Modok": "2024-2025",
        "Spider-Man Far From Home": "2024-2025",
        "Spider-Man Now Way Home": "2024-2025",
        "Venom 2": "2024-2025",
        "Morbius": "2024-2025",
        "Hit Monkey": "2024-2025",
        "The Daily Bugle Saison 2 & 3": "2024-2025",
        "Doctor Strange in the Multiverse of Madness": "2024-2025",
        "Agatha All Along": "2024-2025",
        "Vision Quest": "2024-2025",
        "Hawkeye Saison 1": "2024-2025",
        "Echo Saison 1": "2024-2025",
        "Daredevil: Born Again (Saison 1 et 2)": "2024-2025",
        "Moon Knight Saison 1": "2024-2025",
        "She Hulk Avocate Saison 1": "2024-2025",
        "Miss Marvel Saison 1": "2024-2025",
        "Thor: Love and Thunder": "2024-2025",
        "Black Panther Wakanda Forever": "2024-2025",
        "Spider-Man Across the Spider-Verse": "2024-2025",
        "Spider-Man Beyond the Spider-Verse": "2024-2025",
        "Moon Girl et Devil le Dinosaure Saison 1": "2024-2025",
        "WereWolf by Night": "2024-2025",
        "Les Gardiens de la Galaxie : Joyeuses Fêtes": "2024-2025",

        # Phase 6 : 2024-2026
        "Ant-Man et la Guêpe Quantumania": "2024-2026",
        "Les Gardiens de la Galaxy 3": "2024-2026",
        "Wonder Man": "2025",
        "Secret Invasion Saison 1": "2024-2026",
        "Spider-Man 4": "2026",
        "The Marvels": "2024-2026",
        "Armor Wars (film)": "2024-2026",
        "Loki Saison 2": "2024-2026",
        "What If Et si… le Strange Suprême était intervenu ?": "2024-2026",
        "What If Et si.. Saison 3 Episode 8": "2024-2026",
        "Deadpool et Wolverine": "2024-2026",
        "Marvel Zombies (2025 – animé)": "2025",
        "Captain America: Brave New World": "2024-2026",
        "Thunderbolts": "2024-2026",
        "The Fantastic Four": "2025",
        "Avengers: The Kang Dynasty": "2024-2026",
        "Avengers: Secret Wars": "2027",
    }

    return phase_mapping.get(title, "Inconnue")


for title in titles:
    poster_url = get_poster(title)
    phase = determine_phase(title)
    if phase != "Inconnue":
        if poster_url:
            phases[phase].append({
                "title": title,
                "poster": poster_url
            })
        else:
            phases[phase].append({
                "title": title,
                "poster": "Poster non disponible"
            })


with open("marvel_movies_posters.json", "w", encoding="utf-8") as f:
    json.dump(phases, f, ensure_ascii=False, indent=4)

print("Le fichier JSON a été créé avec succès.")
