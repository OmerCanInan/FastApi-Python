from pydantic import BaseModel

from content_creator.llm import uret


class FonksiyonAciklamasi(BaseModel):
    ad: str
    aciklama: str


class DosyaOzeti(BaseModel):
    genel: str
    fonksiyonlar: list[FonksiyonAciklamasi]


SISTEM = (
    "Sen deneyimli bir Python geliştiricisisin. Sana bir kod dosyası verilecek.\n"
    "genel: Dosyanın ne işe yaradığını 1-2 cümleyle anlat.\n"
    "fonksiyonlar: Dosyadaki her üst seviye fonksiyon ve sınıf için 1-3 cümlelik "
    "Türkçe bir açıklama yaz. Ne yaptığını, önemli sayıları ve kuralları "
    "(ör. kaç kez tekrar denediği, hangi hatalarda ne yaptığı) ve hangi diğer "
    "fonksiyonları kullandığını belirt.\n"
    "'ad' alanına fonksiyonun koddaki adını aynen yaz."
)


def dosya_ozetle(kaynak: str, kod: str) -> DosyaOzeti:
    return uret(
        "hafif",
        f"Dosya: {kaynak}\n\n{kod}",
        sistem=SISTEM,
        sicaklik=0.0,
        sema=DosyaOzeti,
    )