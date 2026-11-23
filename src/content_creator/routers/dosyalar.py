import hashlib

from fastapi import APIRouter, HTTPException, Query, UploadFile
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from content_creator.db import engine
from content_creator.depo import BUCKET, s3
from content_creator.modeller import Dosya

router = APIRouter(tags=["Dosyalar"])


@router.post("/yukle", status_code=201)
async def dosya_yukle(dosya: UploadFile) -> Dosya:
    veri = await dosya.read()
    ozet = hashlib.sha256(veri).hexdigest()
    anahtar = f"yuklenenler/{ozet}"
    try:
        with engine.begin() as b:
            satir = b.execute(
                text("INSERT INTO dosyalar (ad, tur, boyut, hash, depo_anahtari) "
                     "VALUES (:ad, :tur, :boyut, :hash, :depo_anahtari) RETURNING *"),
                {"ad": dosya.filename, "tur": dosya.content_type,
                 "boyut": len(veri), "hash": ozet, "depo_anahtari": anahtar},
            ).one()
            s3.put_object(
                Bucket=BUCKET,
                Key=anahtar,
                Body=veri,
                ContentType=dosya.content_type or "application/octet-stream",
            )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Bu dosya zaten yüklenmiş")
    return Dosya(**satir._mapping)


@router.get("/dosyalar")
def dosyalari_listele() -> list[Dosya]:
    with engine.connect() as b:
        satirlar = b.execute(text("SELECT * FROM dosyalar ORDER BY id")).all()
    return [Dosya(**s._mapping) for s in satirlar]


@router.get("/dosyalar/{dosya_id}/link")
def dosya_linki(dosya_id: int, sure: int = Query(default=600, ge=60, le=3600)) -> dict:
    with engine.connect() as b:
        satir = b.execute(
            text("SELECT depo_anahtari FROM dosyalar WHERE id = :id"), {"id": dosya_id}
        ).first()
    if satir is None:
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")
    if satir.depo_anahtari is None:
        raise HTTPException(status_code=404, detail="Bu dosyanın içeriği depoda yok")
    link = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": satir.depo_anahtari},
        ExpiresIn=sure,
    )
    return {"link": link, "gecerlilik_sn": sure}