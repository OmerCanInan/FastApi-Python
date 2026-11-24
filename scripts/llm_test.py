from content_creator.llm import LLM_MODELLERI, client
from content_creator.llm import uret
from pydantic import BaseModel
from google.genai import types

for rol, model in LLM_MODELLERI.items():
 
    print(rol, "→", model)
print(uret("hafif", "BIST 100'ü tek cümleyle anlat.", sistem="Kısa ve sade cevap ver.", sicaklik=0.0)),




class Degerlendirme(BaseModel):
    dogruluk: int
    dil: int
    hatalar: list[str]


sonuc = uret(
    "elestirmen",
    "Şu metni değerlendir:\n\nBIST 100, ülkemizdeki en güvenilir 100 şirketin dijital skorborddur.",
    sistem="Sen titiz bir finans editörüsün. Metni doğruluk ve dil açısından 1 ile 5 arasında puanla.",
    sicaklik=0.0,
    sema=Degerlendirme,
)
print(sonuc)
