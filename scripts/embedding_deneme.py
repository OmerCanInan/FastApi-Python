from content_creator.embed import vektorle

vektorler = vektorle([
    "THYAO'nun yolcu sayısı üçüncü çeyrekte arttı.",
    "Türk Hava Yolları kaç kişi taşıdı?",
])

print(len(vektorler), "vektör")
print(len(vektorler[0]), "boyut")
print(type(vektorler[0]))