from content_creator.cevap import cevapla

sorular = [
    "Gemini hata verirse kaç kez tekrar deneniyor?",
    "Aynı dosya iki kez yüklenirse ne olur?",
    "Projede hangi ödeme sistemi kullanılıyor?",
]

for soru in sorular:
    sonuc = cevapla(soru)
    print(f"\n? {soru}\n  {sonuc['cevap']}")
    for k in sonuc["kaynaklar"]:
        print(f"  ↳ {k}")