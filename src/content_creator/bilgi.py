from sqlalchemy import text

from content_creator.db import engine
from content_creator.embed import vektorle


def parcalari_kaydet(kaynak: str, metinler: list[str]) -> int:
    vektorler = vektorle(metinler)
    satirlar = [
        {"kaynak": kaynak, "sira": i, "metin": m, "embedding": str(v)}
        for i, (m, v) in enumerate(zip(metinler, vektorler))
    ]
    with engine.begin() as b:
        b.execute(
            text("INSERT INTO parcalar (kaynak, sira, metin, embedding) "
                 "VALUES (:kaynak, :sira, :metin, CAST(:embedding AS vector)) "
                 "ON CONFLICT (kaynak, sira) DO UPDATE "
                 "SET metin = EXCLUDED.metin, embedding = EXCLUDED.embedding"),
            satirlar,
        )
    return len(satirlar)

def ara(soru: str, k: int = 5) -> list[dict]:
    soru_vektoru = str(vektorle([soru])[0])
    with engine.connect() as b:
        satirlar = b.execute(
                        text("SELECT kaynak, sira, metin, "
                 "embedding <=> CAST(:v AS vector) AS uzaklik "
                 "FROM parcalar "
                 "ORDER BY embedding <=> CAST(:v AS vector) "  # YENİ: alias yerine ifade
                 "LIMIT :k"),
            {"v": soru_vektoru, "k": k}
        ).all()
    return [dict(s._mapping) for s in satirlar]