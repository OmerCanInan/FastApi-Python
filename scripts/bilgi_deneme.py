from content_creator.bilgi import ara

sorular = [
    "Dosya yükleme nasıl çalışıyor?",
    "Gemini hata verirse kaç kez tekrar deneniyor?",
    "Projeyi bilgisayarıma nasıl kurarım?",
]

for soru in sorular:
    print(f"\n? {soru}")
    for s in ara(soru, k=3):
        print(f"  {s['puan']:.4f} | {s['kaynak']} #{s['sira']}")