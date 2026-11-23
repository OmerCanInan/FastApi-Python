from fastapi import APIRouter, HTTPException, Query  # YENİ: Query
from sqlalchemy import text

from content_creator.db import engine
from content_creator.modeller import Icerik, IcerikGirdi

router = APIRouter(prefix="/icerikler", tags=["İçerikler"])


@router.post("", status_code=201)
def icerik_olustur(girdi: IcerikGirdi) -> Icerik:
    with engine.begin() as b:
        satir = b.execute(
            text("INSERT INTO icerikler (baslik, platform, adet) "
                 "VALUES (:baslik, :platform, :adet) RETURNING *"),
            girdi.model_dump(),
        ).one()
    return Icerik(**satir._mapping)


@router.get("")
def icerikleri_listele(platform: str | None = None,
    limit: int = Query(default=10, ge=1, le=100)) -> list[Icerik]:  # YENİ
    sql = "SELECT * FROM icerikler"
    parametreler = {"limit": limit}
    if platform:
        sql += " WHERE platform = :platform"
        parametreler["platform"] = platform
    sql += " ORDER BY id LIMIT :limit"
    with engine.connect() as b:
        satirlar = b.execute(text(sql), parametreler).all()
    return [Icerik(**s._mapping) for s in satirlar]


@router.get("/{icerik_id}")
def icerik_getir(icerik_id: int) -> Icerik:
    with engine.connect() as b:
        satir = b.execute(
            text("SELECT * FROM icerikler WHERE id = :id"), {"id": icerik_id}
        ).first()
    if satir is None:
        raise HTTPException(status_code=404, detail="İçerik bulunamadı")
    return Icerik(**satir._mapping)