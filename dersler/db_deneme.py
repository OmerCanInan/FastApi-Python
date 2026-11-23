import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def icerik_kaldir(baglanti) -> bool:
    id = input("Silinecek içerik ID'si: ")
    sonuc = baglanti.execute(text("DELETE FROM icerikler WHERE id = :id"), {"id": id})
    return sonuc.rowcount > 0

DB_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DB_URL)

with engine.begin() as baglanti:
    icerik_kaldir(baglanti)
    sonuc = baglanti.execute(text("SELECT * FROM icerikler"))
    for satir in sonuc:
        print(satir)


        