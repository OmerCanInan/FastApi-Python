import hashlib  # YENİ
import os
from datetime import datetime


import boto3  # YENİ
from botocore.config import Config  # YENİ
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, UploadFile  # YENİ
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError  # YENİ

load_dotenv()  # YENİ
DB_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)  # YENİ
engine = create_engine(DB_URL)  # YENİ
BUCKET = os.environ["S3_BUCKET"]  # YENİ
s3 = boto3.client(  # YENİ
    "s3",
    endpoint_url=os.environ["S3_ENDPOINT"],
    region_name=os.environ["S3_REGION"],
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
       config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),  # YENİ
)
app = FastAPI(title="Content Creator API")


class IcerikGirdi(BaseModel):
    baslik: str = Field(min_length=3, max_length=100)
    platform: str
    adet: int = Field(default=1, ge=1, le=10)


class Icerik(IcerikGirdi):
    id: int
    olusturma: datetime  # YENİ

class Dosya(BaseModel):
    id: int
    ad: str
    tur: str | None
    boyut: int
    hash: str
    yuklenme: datetime
    depo_anahtari: str | None  # YENİ
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


@app.post("/yukle", status_code=201)
async def dosya_yukle(dosya: UploadFile) -> Dosya:
    veri = await dosya.read()
    ozet = hashlib.sha256(veri).hexdigest()
    anahtar = f"yuklenenler/{ozet}"  # YENİ
    s3.put_object(  # YENİ
        Bucket=BUCKET,  # YENİ
        Key=anahtar,  # YENİ
        Body=veri,  # YENİ
        ContentType=dosya.content_type or "application/octet-stream",  # YENİ
    )  # YENİ
    try:
        with engine.begin() as b:
            satir = b.execute(
                text("INSERT INTO dosyalar (ad, tur, boyut, hash, depo_anahtari) "  # YENİ
                     "VALUES (:ad, :tur, :boyut, :hash, :depo_anahtari) RETURNING *"),  # YENİ
                {"ad": dosya.filename, "tur": dosya.content_type,
                 "boyut": len(veri), "hash": ozet, "depo_anahtari": anahtar},  # YENİ
            ).one()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Bu dosya zaten yüklenmiş")
    return Dosya(**satir._mapping)

@app.get("/dosyalar")  # YENİ
def dosyalari_listele() -> list[Dosya]:  # YENİ
    with engine.connect() as b:  # YENİ
        satirlar = b.execute(text("SELECT * FROM dosyalar ORDER BY id")).all()  # YENİ
    return [Dosya(**s._mapping) for s in satirlar]  # YENİ

@app.get("/dosyalar/{dosya_id}/link")  # YENİ
def dosya_linki(dosya_id: int, sure: int = Query(default=600, ge=60, le=3600)) -> dict:  # YENİ
    with engine.connect() as b:  # YENİ
        satir = b.execute(  # YENİ
            text("SELECT depo_anahtari FROM dosyalar WHERE id = :id"), {"id": dosya_id}  # YENİ
        ).first()  # YENİ
    if satir is None:  # YENİ
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")  # YENİ
    if satir.depo_anahtari is None:  # YENİ
        raise HTTPException(status_code=404, detail="Bu dosyanın içeriği depoda yok")  # YENİ
    link = s3.generate_presigned_url(  # YENİ
        "get_object",  # YENİ
        Params={"Bucket": BUCKET, "Key": satir.depo_anahtari},  # YENİ
        ExpiresIn=sure,  # YENİ
    )  # YENİ
    return {"link": link, "gecerlilik_sn": sure}  # YENİ
