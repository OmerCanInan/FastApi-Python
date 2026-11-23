import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

TEKRAR_DENENEBILIR = {429, 500, 503}


def uret(model: str, icerik: str, deneme: int = 3) -> str:
    for i in range(deneme):
        try:
            cevap = client.models.generate_content(model=model, contents=icerik)
            return cevap.text
        except errors.APIError as hata:
            if hata.code not in TEKRAR_DENENEBILIR:
                raise
            bekle = 2 ** i
            print(f"{hata.code} geldi, {bekle} sn bekliyorum")
            time.sleep(bekle)
    raise RuntimeError("Tüm denemeler başarısız")


print(uret(os.environ["GEMINI_MODEL_HAFIF"], "Merhaba, tek kelimeyle cevap ver."))