import json
import time
from pathlib import Path

from pydantic import BaseModel

from content_creator.cevap import cevapla
from content_creator.llm import uret

YOK = "bilgi tabanında bu bilgi yok"
BEKLEME = 8


class HakemKarari(BaseModel):
    dogru: bool
    gerekce: str


HAKEM_SISTEM = (
    "Sen titiz bir değerlendiricisin. Sana bir soru, beklenen cevap ve modelin cevabı verilecek.\n"
    "Modelin cevabı beklenen cevaptaki temel bilgiyi (sayılar, adlar, kurallar) doğru "
    "içeriyorsa dogru=true, eksik veya yanlışsa dogru=false yaz. "
    "Fazladan doğru bilgi hata sayılmaz.\n"
    "gerekce alanına tek cümlelik Türkçe bir açıklama yaz."
)


def cevap_dogru_mu(soru: str, beklenen: str, cevap: str) -> tuple[bool, str]:
    karar = uret(
        "hafif",
        f"Soru: {soru}\nBeklenen: {beklenen}\nModelin cevabı: {cevap}",
        sistem=HAKEM_SISTEM,
        sicaklik=0.0,
        sema=HakemKarari,
    )
    return karar.dogru, karar.gerekce


def kaynak_dogru_mu(beklenen_kaynak: str | None, kaynaklar: list[str]) -> bool:
    if beklenen_kaynak is None:
        return not kaynaklar
    return any(k.split(" #")[0] == beklenen_kaynak for k in kaynaklar)
sorular = json.loads(Path("scripts/eval_sorular.json").read_text(encoding="utf-8"))
gecen = 0

for i, s in enumerate(sorular, start=1):
    try:
        sonuc = cevapla(s["soru"])
        if s["kaynak"] is None:
            cevap_ok, gerekce = YOK in sonuc["cevap"].lower(), "cevapsız soru"
        else:
            cevap_ok, gerekce = cevap_dogru_mu(s["soru"], s["beklenen"], sonuc["cevap"])
        kaynak_ok = kaynak_dogru_mu(s["kaynak"], sonuc["kaynaklar"])
    except Exception as hata:
        sonuc, cevap_ok, kaynak_ok, gerekce = None, False, False, f"hata: {hata}"

    ok = cevap_ok and kaynak_ok
    gecen += ok
    print(f"{'✅' if ok else '❌'} {i:2}. {s['soru']}")
    if not ok:
        print(f"     cevap ok: {cevap_ok} | kaynak ok: {kaynak_ok} | {gerekce}")
        if sonuc:
            print(f"     cevap: {sonuc['cevap']}")
            print(f"     kaynaklar: {sonuc['kaynaklar']}")
    time.sleep(BEKLEME)

print(f"\nSonuç: {gecen}/{len(sorular)}  (kapı: 16)")