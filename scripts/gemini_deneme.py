import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL_HAFIF"]


class Degerlendirme(BaseModel):
    dogruluk: int
    dil: int
    hatalar: list[str]


TASLAK = (
    "BIST 100, ülkemizdeki en büyük ve en güvenilir 100 şirketin hisselerinin "
    "fiyatlarının ortalama durumunu gösteren bir dijital skorborddur."
)

cevap = client.models.generate_content(
    model=MODEL,
    contents=f"Şu metni değerlendir:\n\n{TASLAK}",
    config=types.GenerateContentConfig(
        system_instruction=(
    "Sen titiz bir finans editörüsün. Metni iki açıdan 1 ile 5 arasında puanla.\n"
    "dogruluk: Finansal bilgiler doğru mu? Yanlış, eksik ya da abartılı iddia var mı?\n"
    "dil: Doğal ve hatasız Türkçe mi? Şunlar dil hatasıdır: yazım hatası, "
    "İngilizceden geçmiş kelimeler (ör. skorbord, revenue), çeviri kokan cümle yapısı.\n"
    "Her hatayı ayrı madde olarak yaz ve başına [DOĞRULUK] ya da [DİL] etiketi koy."
),
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=Degerlendirme,
    ),
)

print(cevap.text)

sonuc = cevap.parsed
print("Doğruluk:", sonuc.dogruluk)
print("Dil:", sonuc.dil)
for hata in sonuc.hatalar:
    print("-", hata)