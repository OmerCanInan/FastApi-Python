from fastapi import FastAPI

from content_creator.routers import dosyalar, icerikler, sor

app = FastAPI(title="Content Creator API")
app.include_router(icerikler.router)
app.include_router(dosyalar.router)
app.include_router(sor.router)
    


@app.get("/", tags=["Sağlık"])
def saglik() -> dict:
    return {"durum": "çalışıyor"}