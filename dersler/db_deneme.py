import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DB_URL)

with engine.connect() as baglanti:
    sonuc = baglanti.execute(text("SELECT * FROM icerikler"))
    for satir in sonuc:
        print(satir)