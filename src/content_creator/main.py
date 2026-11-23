from fastapi import FastAPI

from content_creator.routers import dosyalar, icerikler

app = FastAPI(title="Content Creator API")
app.include_router(icerikler.router)
app.include_router(dosyalar.router)


@app.get("/", tags=["Sağlık"])
def saglik() -> dict:
    return {"durum": "çalışıyor"}