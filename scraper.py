import os
import pandas as pd
import requests
from datetime import datetime

print(">>> Mengekstrak data Kedai Kopi Bali via OpenStreetMap API...")

# API Pencarian Lokasi Spasial
url = "https://nominatim.openstreetmap.org/search.php?q=coffee+shop+in+bali&format=jsonv2&limit=30"
headers = {'User-Agent': 'Portfolio-Scraper-App/1.0'}

response = requests.get(url, headers=headers)
data = response.json()

data_hasil = []
for item in data:
    data_hasil.append({
        "tanggal_update": datetime.now().strftime("%Y-%m-%d"),
        "nama_tempat": item.get("display_name", "").split(",")[0],
        "alamat_lengkap": item.get("display_name", ""),
        "latitude": item.get("lat", ""),
        "longitude": item.get("lon", "")
    })

df = pd.DataFrame(data_hasil)
df.to_csv('dataset_direktori_kedai.csv', index=False)
print(f"  Berhasil menyimpan {len(df)} baris data ke CSV.")

os.system('git add .')
os.system(f'git commit -m "Update Direktori Kedai Kopi: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')
os.system('git push origin main >nul 2>&1')
print("✅ Repo DirektoriKedai berhasil di-push!")