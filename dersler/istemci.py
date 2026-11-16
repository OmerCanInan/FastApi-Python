import httpx

URL = "http://127.0.0.1:8000/icerikler"

for baslik, platform in [("Async ile hız", "linkedin"),  # YENİ
                         ("Semaphore nedir", "x"),  # YENİ
                         ("FastAPI ilk adım", "linkedin")]:  # YENİ
    httpx.post(URL, json={"baslik": baslik, "platform": platform})  # YENİ

r = httpx.get(URL)  # YENİ
print("Hepsi:", r.json())  # YENİ

r = httpx.get(URL, params={"platform": "linkedin"})  # YENİ
print("LinkedIn:", r.json())  # YENİ
print("İstek atılan URL:", r.url)  # YENİ

r = httpx.get(f"{URL}/2")  # YENİ
print(r.status_code, r.json())  # YENİ

r = httpx.get(f"{URL}/99")  # YENİ
print(r.status_code, r.json())  # YENİ

with open("pyproject.toml", "rb") as f:  # YENİ
    r = httpx.post("http://127.0.0.1:8000/yukle", files={"dosya": f})  # YENİ
print(r.status_code, r.json())  # YENİ