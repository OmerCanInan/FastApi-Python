import time                                          # YENİ
import httpx
import base64

def istek_at(url: str, deneme: int = 3) -> dict:
    for i in range(deneme):
        print(f"Deneme {i + 1}")
        r = httpx.get(url, timeout=10)
        if r.status_code == 429 or r.status_code >= 500:   # YENİ: 429 da eklendi
            bekle = 2 ** i                                   # YENİ
            print(f"{r.status_code} geldi, {bekle} sn bekliyorum")   # YENİ
            time.sleep(bekle)                                # YENİ
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Tüm denemeler başarısız")

SAHIP = "OmerCanInan"
REPO = "Gundemim"

def dosya_listesi(sahip: str, repo: str, klasor: str = "") -> list[str]:
    agac = istek_at(f"https://api.github.com/repos/{sahip}/{repo}/git/trees/HEAD?recursive=1")
    return [o["path"] for o in agac["tree"]
            if o["type"] == "blob" and o["path"].startswith(klasor)]


def dosya_oku(sahip: str, repo: str, yol: str) -> str:
    dosya = istek_at(f"https://api.github.com/repos/{sahip}/{repo}/contents/{yol}")
    return base64.b64decode(dosya["content"]).decode("utf-8")


yollar = dosya_listesi(SAHIP, REPO, "src/services/")
print(len(yollar), "dosya bulundu")

for yol in yollar:
    kod = dosya_oku(SAHIP, REPO, yol)
    print(f"{yol}: {len(kod.splitlines())} satır")
    print(kod, "...\n")
