from fastapi import APIRouter, HTTPException

from content_creator.cevap import cevapla
from content_creator.modeller import SoruCevabi, SoruGirdi

router = APIRouter(tags=["Soru"])


@router.post("/sor")
def sor(girdi: SoruGirdi) -> SoruCevabi:
    try:
        sonuc = cevapla(girdi.soru)
    except (RuntimeError, ValueError):
        raise HTTPException(status_code=503, detail="Model şu an cevap veremiyor, biraz sonra dene")
    return SoruCevabi(**sonuc)