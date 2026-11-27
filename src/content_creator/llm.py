import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, ValidationError

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options=types.HttpOptions(
        timeout=60_000,
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
)

LLM_MODELLERI = {
    "yazar": os.environ["GEMINI_MODEL_YAZAR"],
    "hafif": os.environ["GEMINI_MODEL_HAFIF"],
    "elestirmen": os.environ["GEMINI_MODEL_ELESTIRMEN"],
}

TEKRAR_DENENEBILIR = {429, 500, 503}


def _json_ayikla(metin: str) -> str:
    metin = metin.strip()
    if metin.startswith("```"):
        metin = metin.split("\n", 1)[1]
    if metin.endswith("```"):
        metin = metin[:-3]
    return metin.strip()


def uret(rol: str, icerik: str, sistem: str | None = None,
         sicaklik: float = 0.7, sema: type[BaseModel] | None = None,
         deneme: int = 3):
    ayar = types.GenerateContentConfig(
        system_instruction=sistem,
        temperature=sicaklik,
        response_mime_type="application/json" if sema else None,
        response_schema=sema,
    )
    son_hata = None
    for i in range(deneme):
        try:
            cevap = client.models.generate_content(
                model=LLM_MODELLERI[rol], contents=icerik, config=ayar
            )
            if not cevap.text:
                sebep = cevap.candidates[0].finish_reason if cevap.candidates else "aday yok"
                raise ValueError(f"Model boş cevap döndü. Sebep: {sebep}")
            if sema is None:
                return cevap.text
            try:
                return sema.model_validate_json(_json_ayikla(cevap.text))
            except ValidationError:
                raise ValueError(f"Cevap şemaya uymadı: {cevap.text!r}")
        except errors.APIError as hata:
            if hata.code not in TEKRAR_DENENEBILIR:
                raise
            son_hata = hata
            time.sleep(2 ** i)
    raise RuntimeError(
        f"{deneme} deneme başarısız. Son hata {son_hata.code}: {son_hata.message}"
    ) from son_hata
