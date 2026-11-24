from sentence_transformers import SentenceTransformer

MODEL_ADI = "BAAI/bge-m3"
BOYUT = 1024

_model = None


def _model_getir() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_ADI)
    return _model


def vektorle(metinler: list[str]) -> list[list[float]]:
    vektorler = _model_getir().encode(metinler, normalize_embeddings=True)
    return vektorler.tolist()