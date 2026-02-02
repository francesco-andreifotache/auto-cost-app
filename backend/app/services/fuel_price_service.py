import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_fuel_price(fuel_type: str) -> float:
    # 1. Încercăm să luăm prețul real
    try:
        api_key = os.getenv("COLLECT_API_KEY")
        if not api_key:
            raise ValueError("Lipseste cheia API")

        url = "https://api.collectapi.com/gasPrice/europeanCountries"
        headers = {
            "content-type": "application/json",
            "authorization": api_key
        }
        
        # Facem cererea
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Aici dadea eroare inainte
        
        data = response.json()
        
        # Caută prețul pentru Romania (sau ce logica ai tu acolo)
        # Aici e un exemplu simplificat, adapteaza dupa cum parsezi tu JSON-ul
        # De exemplu, daca returnezi mereu un pret hardcodat temporar:
        return 7.5 

    except Exception as e:
        # 2. PLASA DE SIGURANȚĂ
        # Dacă orice merge prost (nu ai net, cheia e gresita, site-ul e picat)
        # afisam eroarea in consola, dar returnam un preț mediu ca aplicația să meargă.
        print(f"⚠️ Eroare la preluarea pretului carburant: {e}")
        print("➡️ Folosesc pretul default de 7.5 RON")
        
        return 7.5 # Returnam un preț mediu (7.5 RON) ca sa nu crape calculul