from pathlib import Path

from content_creator.bilgi import parcalari_kaydet
from content_creator.ozetle import dosya_ozetle
from content_creator.parcala import kod_parcala, metin_parcala


def kod_parcalari(kaynak: str, metin: str) -> list[str]:
    try:
        ozet = dosya_ozetle(kaynak, metin)
    except Exception as hata:
        print(f"  özet alınamadı ({hata.__class__.__name__}), açıklamasız devam")
        return [f"Dosya: {kaynak}\n\n{kod}" for _, kod in kod_parcala(metin)]

    aciklamalar = {f.ad: f.aciklama for f in ozet.fonksiyonlar}
    parcalar = []
    for ad, kod in kod_parcala(metin):
        aciklama = ozet.genel if ad == "_ust" else aciklamalar.get(ad, "")
        parcalar.append(f"Dosya: {kaynak}\nAçıklama: {aciklama}\n\n{kod}")
    return parcalar


dosyalar = [Path("README.md"), *sorted(Path("src").rglob("*.py"))]

for dosya in dosyalar:
    kaynak = dosya.as_posix()
    metin = dosya.read_text(encoding="utf-8")
    if not metin.strip():
        print(f"  atlandı | {kaynak}")
        continue
    if dosya.suffix == ".py":
        parcalar = kod_parcalari(kaynak, metin)
    else:
        parcalar = [f"Dosya: {kaynak}\n\n{p}" for p in metin_parcala(metin)]
    adet = parcalari_kaydet(kaynak, parcalar)
    print(f"{adet:3} parça | {kaynak}")