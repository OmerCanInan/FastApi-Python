from pathlib import Path

from content_creator.bilgi import parcalari_kaydet
from content_creator.parcala import kod_parcala, metin_parcala

dosyalar = [Path("README.md"), *sorted(Path("src").rglob("*.py"))]

for dosya in dosyalar:
    kaynak = dosya.as_posix()
    metin = dosya.read_text(encoding="utf-8")
    if dosya.suffix == ".py":
        parcalar = kod_parcala(metin)
    else:
        parcalar = metin_parcala(metin)
    if not parcalar:
        print(f"  atlandı | {kaynak}")
        continue
    parcalar = [f"Dosya: {kaynak}\n\n{p}" for p in parcalar]
    adet = parcalari_kaydet(kaynak, parcalar)
    print(f"{adet:3} parça | {kaynak}")