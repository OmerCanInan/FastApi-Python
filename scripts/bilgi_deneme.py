from content_creator.bilgi import ara

sorular = [
    "Kod parçalarının başındaki açıklamalar nereden geliyor?",
    "Soru cevaplanırken modelin bilgi uydurması nasıl engelleniyor?",
]

for soru in sorular:
    print(f"\n? {soru}")
    for s in ara(soru, k=5):
        print(f"  {s['puan']:.4f} | {s['kaynak']} #{s['sira']}")