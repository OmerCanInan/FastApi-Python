from content_creator.bilgi import ara
from content_creator.bilgi import kelime_ara

sorular = [
    "Dosya yükleme nasıl çalışıyor?",
    "Gemini hata verirse kaç kez tekrar deneniyor?",
    "Projeyi bilgisayarıma nasıl kurarım?",
]

for soru in sorular:
    print(f"\n? {soru}")
    for s in ara(soru, k=3):
        print(f"  {s['uzaklik']:.3f} | {s['kaynak']} #{s['sira']}")

print("\n--- KELİME ARAMASI ---")
for s in kelime_ara("Gemini hata verirse kaç kez tekrar deneniyor?", k=3):
    print(f"  {s['skor']:.3f} | {s['kaynak']} #{s['sira']}")