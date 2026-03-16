import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import PesticideRegistry

def init_pesticide_db():
    print("Membaca file Excel pestisida_bersih.xlsx...")
    try:
        df = pd.read_excel('../pestisida_bersih.xlsx')
    except Exception as e:
        print(f"Gagal membaca file Excel: {e}")
        return

    print("Membuat koneksi ke database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Cek apakah tabel sudah berisi data
        existing_count = db.query(PesticideRegistry).count()
        if existing_count > 0:
            print(f"Tabel PesticideRegistry sudah berisi {existing_count} baris. Lewati inisialisasi.")
            return

        print(f"Memproses {len(df)} baris data...")
        
        # Batch processing untuk efisiensi memori (penting karena 4000+ data bisa memperlambat)
        batch_size = 1000
        records = []
        count = 0
        
        for index, row in df.iterrows():
            nama = str(row['Nama Produk']).strip() if pd.notna(row['Nama Produk']) else "Tidak Diketahui"
            
            # Abaikan baris kosong
            if nama == "Tidak Diketahui" or nama == "" or nama.lower() == "nan":
                continue
                
            kategori = str(row['Jenis Pestisida']).strip() if pd.notna(row['Jenis Pestisida']) else None
            perusahaan = str(row['Nama Perusahaan']).strip() if pd.notna(row['Nama Perusahaan']) else None
            bahan_aktif = str(row['Bahan Aktif']).strip() if pd.notna(row['Bahan Aktif']) else None

            pes = PesticideRegistry(
                nama_pestisida=nama,
                kategori=kategori,
                nama_perusahaan=perusahaan,
                bahan_aktif=bahan_aktif
            )
            records.append(pes)
            count += 1
            
            if count % batch_size == 0:
                db.add_all(records)
                db.commit()
                records = []
                print(f"Tersimpan {count} baris...")

        # Commit sisa data
        if records:
            db.add_all(records)
            db.commit()
            print(f"Tersimpan {count} baris...")
            
        final_count = db.query(PesticideRegistry).count()
        print(f"Selesai! Berhasil menyimpan total {final_count} data pestisida ke database SQLite.")
        
    except Exception as e:
        db.rollback()
        print(f"Terjadi kesalahan saat menyimpan ke database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_pesticide_db()
