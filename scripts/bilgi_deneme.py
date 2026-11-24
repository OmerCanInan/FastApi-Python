from content_creator.bilgi import ara, parcalari_kaydet

notlar = [
    "THYAO 3. çeyrekte yolcu sayısını yüzde 8 artırdı.",
    "TAV Havalimanları dış hat yolcu trafiğinde rekor kırdı.",
    "FastAPI ile dosya yükleme endpoint'i yazdık.",
    "Semaphore aynı anda çalışan istek sayısını sınırlar.",
    "Karnıyarık için patlıcanları önce kızartın.",
]

print(parcalari_kaydet("deneme/notlar", notlar), "parça kaydedildi")

for sonuc in ara("Aynı anda kaç API isteği atabilirim?", k=3):
    print(round(sonuc["uzaklik"], 3), "|", sonuc["metin"])