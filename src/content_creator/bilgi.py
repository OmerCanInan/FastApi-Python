from sqlalchemy import text

from content_creator.db import engine
from content_creator.embed import vektorle


def parcalari_kaydet(kaynak: str, metinler: list[str]) -> int:
    vektorler = vektorle(metinler)
    satirlar = [
        {"kaynak": kaynak, "sira": i, "metin": m, "embedding": str(v)}
        for i, (m, v) in enumerate(zip(metinler, vektorler))
    ]
    with engine.begin() as baglanti:
        baglanti.execute(
            text("DELETE FROM parcalar WHERE kaynak = :kaynak"),
            {"kaynak": kaynak},
        )
        baglanti.execute(
            text("""
                INSERT INTO parcalar (kaynak, sira, metin, embedding)
                VALUES (:kaynak, :sira, :metin, CAST(:embedding AS vector))
            """),
            satirlar,
        )
    return len(satirlar)


def anlam_ara(soru: str, k: int = 5) -> list[dict]:
    soru_vektoru = str(vektorle([soru])[0])
    sorgu = text("""
        SELECT kaynak, sira, metin, embedding <=> CAST(:v AS vector) AS uzaklik
        FROM parcalar
        ORDER BY embedding <=> CAST(:v AS vector)
        LIMIT :k
    """)
    with engine.connect() as baglanti:
        satirlar = baglanti.execute(sorgu, {"v": soru_vektoru, "k": k}).mappings().all()
    return [dict(s) for s in satirlar]


def kelime_ara(soru: str, k: int = 5) -> list[dict]:
    sorgu = text("""
        SELECT kaynak, sira, metin, ts_rank(arama, q) AS skor
        FROM parcalar,
             to_tsquery('turkish',
                 replace(plainto_tsquery('turkish', :soru)::text, ' & ', ' | ')) AS q
        WHERE arama @@ q
        ORDER BY skor DESC
        LIMIT :k
    """)
    with engine.connect() as baglanti:
        satirlar = baglanti.execute(sorgu, {"soru": soru, "k": k}).mappings().all()
    return [dict(s) for s in satirlar]

RRF_K = 60


def ara(soru: str, k: int = 5) -> list[dict]:
    listeler = [anlam_ara(soru, k=20), kelime_ara(soru, k=20)]
    puanlar = {}
    metinler = {}
    for liste in listeler:
        for sira, p in enumerate(liste, start=1):
            anahtar = (p["kaynak"], p["sira"])
            puanlar[anahtar] = puanlar.get(anahtar, 0) + 1 / (RRF_K + sira)
            metinler[anahtar] = p["metin"]
    en_iyiler = sorted(puanlar, key=puanlar.get, reverse=True)[:k]
    return [
        {"kaynak": a[0], "sira": a[1], "metin": metinler[a], "puan": puanlar[a]}
        for a in en_iyiler
    ]