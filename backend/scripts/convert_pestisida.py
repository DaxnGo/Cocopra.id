import pandas as pd
import json

df = pd.read_excel('pestisida_bersih.xlsx')

def clean_val(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

data = []
for index, row in df.iterrows():
    name = clean_val(row.get('Nama Produk'))
    if not name:
        continue
        
    expiry = clean_val(row.get('Tanggal Berakhir'))
    # Very basic status check: if it has expiry it's likely active
    status = "aktif"
    if "cabut" in expiry.lower() or "dilarang" in expiry.lower() or "ilegal" in expiry.lower():
        status = "ilegal"
    
    # We can truncate or clean Target Crop to save size
    target_crop = clean_val(row.get('Komoditas & Hama'))
    if len(target_crop) > 50:
        target_crop = target_crop[:47] + "..."

    item = {
        "id": index + 1,
        "name": name,
        "regNumber": clean_val(row.get('Nomor Pendaftaran')),
        "company": clean_val(row.get('Nama Perusahaan')),
        "activeIngredient": clean_val(row.get('Bahan Aktif')),
        "category": clean_val(row.get('Jenis Pestisida')),
        "formulation": clean_val(row.get('Bentuk Formulasi')),
        "targetCrop": target_crop,
        "expiry": expiry,
        "status": status
    }
    data.append(item)

print(f"Total entries parsed: {len(data)}")

with open('PROXO/public/pestisida.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print("JSON file created at PROXO/public/pestisida.json")
