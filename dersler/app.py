import hashlib  # YENİ
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError  # YENİ

load_dotenv()  # YENİ
DB_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)  # YENİ
engine = create_engine(DB_URL)  # YENİ

app = FastAPI(title="Content Creator API")


class IcerikGirdi(BaseModel):
    baslik: str = Field(min_length=3, max_length=100)
    platform: str
    adet: int = Field(default=1, ge=1, le=10)


class Icerik(IcerikGirdi):
    id: int
    olusturma: datetime  # YENİ

class Dosya(BaseModel):  # YENİ
    id: int
    ad: str
    tur: str | None
    boyut: int
    hash: str
    yuklenme: datetime

@app.get("/")
def saglik() -> dict:
    return {"durum": "çalışıyor"}


@app.post("/icerikler", status_code=201)
def icerik_olustur(girdi: IcerikGirdi) -> Icerik:
    with engine.begin() as b:  # YENİ
        satir = b.execute(  # YENİ
            text("INSERT INTO icerikler (baslik, platform, adet) "  # YENİ
                 "VALUES (:baslik, :platform, :adet) RETURNING *"),  # YENİ
            girdi.model_dump(),  # YENİ
        ).one()  # YENİ
    return Icerik(**satir._mapping)  # YENİ


@app.get("/icerikler")
def icerikleri_listele(platform: str | None = None, limit: int = 10) -> list[Icerik]:
    sql = "SELECT * FROM icerikler"  # YENİ
    parametreler = {"limit": limit}  # YENİ
    if platform:
        sql += " WHERE platform = :platform"  # YENİ
        parametreler["platform"] = platform  # YENİ
    sql += " ORDER BY id LIMIT :limit"  # YENİ
    with engine.connect() as b:  # YENİ
        satirlar = b.execute(text(sql), parametreler).all()  # YENİ
    return [Icerik(**s._mapping) for s in satirlar]  # YENİ


@app.get("/icerikler/{icerik_id}")
def icerik_getir(icerik_id: int) -> Icerik:
    with engine.connect() as b:  # YENİ
        satir = b.execute(  # YENİ
            text("SELECT * FROM icerikler WHERE id = :id"), {"id": icerik_id}  # YENİ
        ).first()  # YENİ
    if satir is None:  # YENİ
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")
    return Icerik(**satir._mapping)  # YENİ


@app.post("/yukle", status_code=201)  # YENİ
async def dosya_yukle(dosya: UploadFile) -> Dosya:  # YENİ
    veri = await dosya.read()
    ozet = hashlib.sha256(veri).hexdigest()  # YENİ
    try:  # YENİ
        with engine.begin() as b:  # YENİ
            satir = b.execute(  # YENİ
                text("INSERT INTO dosyalar (ad, tur, boyut, hash) "  # YENİ
                     "VALUES (:ad, :tur, :boyut, :hash) RETURNING *"),  # YENİ
                {"ad": dosya.filename, "tur": dosya.content_type,  # YENİ
                 "boyut": len(veri), "hash": ozet},  # YENİ
            ).one()  # YENİ
    except IntegrityError:  # YENİ
        raise HTTPException(status_code=409, detail="Bu dosya zaten yüklenmiş")  # YENİ
    return Dosya(**satir._mapping)  # YENİ


@app.get("/dosyalar")  # YENİ
def dosyalari_listele() -> list[Dosya]:  # YENİ
    with engine.connect() as b:  # YENİ
        satirlar = b.execute(text("SELECT * FROM dosyalar ORDER BY id")).all()  # YENİ
    return [Dosya(**s._mapping) for s in satirlar]  # YENİ