from datetime import datetime

from pydantic import BaseModel, Field


class IcerikGirdi(BaseModel):
    baslik: str = Field(min_length=3, max_length=100)
    platform: str
    adet: int = Field(default=1, ge=1, le=10)


class Icerik(IcerikGirdi):
    id: int
    olusturma: datetime
    durum: str


class Dosya(BaseModel):
    id: int
    ad: str
    tur: str | None
    boyut: int
    hash: str
    yuklenme: datetime
    depo_anahtari: str | None

class SoruGirdi(BaseModel):
    soru: str = Field(min_length=3, max_length=500)


class SoruCevabi(BaseModel):
    cevap: str
    kaynaklar: list[str]