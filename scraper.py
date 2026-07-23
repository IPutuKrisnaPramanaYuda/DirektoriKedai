import os
import pandas as pd
import requests
from datetime import datetime

print(">>> Mengekstrak data Kedai Kopi Bali via OpenStreetMap API...")

queries = [
    "coffee shop in Denpasar Selatan, Bali",
    "coffee shop in Denpasar Barat, Bali",
    "coffee shop in Denpasar Timur, Bali",
    "coffee shop in Denpasar Utara, Bali",
    "coffee shop in Sanur, Bali",
    "coffee shop in Renon, Bali",
    "coffee shop in Kuta, Bali",
    "coffee shop in Seminyak, Bali",
    "coffee shop in Canggu, Bali",
    "coffee shop in Jimbaran, Bali",
    "coffee shop in Nusa Dua, Bali",
    "coffee shop in Uluwatu, Bali",
    "coffee shop in Ubud, Bali",
    "coffee shop in Gianyar, Bali",
    "coffee shop in Tabanan, Bali",
    "coffee shop in Singaraja, Bali",
    "coffee shop in Kintamani, Bali",
    "coffee shop in Mengwi, Bali",
    "coffee shop in Amed, Bali"
]
headers = {'User-Agent': 'Portfolio-Scraper-App/1.0'}

data_hasil = []
seen_places = set()

for query in queries:
    print(f"  -> Mencari: {query}")
    url = f"https://nominatim.openstreetmap.org/search.php?q={query.replace(' ', '+')}&format=jsonv2&limit=50"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for item in data:
            place_id = item.get("place_id")
            if place_id and place_id not in seen_places:
                seen_places.add(place_id)
                data_hasil.append({
                    "tanggal_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nama_tempat": item.get("display_name", "").split(",")[0],
                    "alamat_lengkap": item.get("display_name", ""),
                    "latitude": item.get("lat", ""),
                    "longitude": item.get("lon", "")
                })
    except Exception as e:
        print(f"Error scraping {query}: {e}")

df = pd.DataFrame(data_hasil)
df.to_csv('dataset_direktori_kedai.csv', index=False)
print(f"  Berhasil menyimpan {len(df)} baris data unik ke CSV.")

os.system('git add .')
os.system(f'git commit -m "Update Direktori Kedai Kopi: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')
os.system('git push origin main >nul 2>&1')
print("[SUKSES] Repo DirektoriKedai berhasil di-push!")