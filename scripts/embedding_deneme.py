from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")
print("Model yüklendi")

cumleler = [
    "THYAO'nun yolcu sayısı üçüncü çeyrekte arttı.",
    "Türk Hava Yolları kaç kişi taşıdı?",
    "Karnıyarık nasıl yapılır?",
]

vektorler = model.encode(cumleler, normalize_embeddings=True)

print(vektorler.shape)
print(vektorler[0][:5])

benzerlik = vektorler @ vektorler.T
print(benzerlik.round(3))