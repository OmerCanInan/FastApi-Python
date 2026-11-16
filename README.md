# AI Content Creator

Yükledigim dosya, proje ve fotograflardan ögrenip **her hafta kendi kendine içerik paketi üreten** bir sistem.
Bütçe sifir: ücretsiz katmanlar, açik kaynak modeller ve kendi donanimim.

> **Durum:** Faz 1 (egitim) · Hafta 2 tamamlaniyor. Bu repo su an hem ögrenme defteri (dersler/) hem de projenin ilk backend'i.

---

## Hedef mimari

`
Kaynaklar (PDF, repo, fotograf)
   ¦  dizüstü: bge-m3 embedding, Florence-2 / Qwen2.5-VL (4-bit)
   ?
Neon (Postgres + pgvector)  ?--?  FastAPI backend  ?--  Streamlit panel / Telegram onayi
   ?                                   ¦
   ¦                                   ?
GitHub Actions (haftalik cron) --? Gemini (metin) · Cloudflare Workers AI (görsel) · R2 (dosyalar)
`

Kisisel model üç katmanli, sifirdan egitim yok:
**RAG** (bilgi) ? **stil profili + few-shot** (ses) ? yeterli veri birikince **LoRA** (stil).

---

## Su an çalisan kisim

FastAPI + Neon üzerinde, içerik kaydi ve dosya yükleme yapan bir API.

| Metot | Endpoint | Ne yapar |
|---|---|---|
| GET | / | Saglik kontrolü |
| POST | /icerikler | Içerik olusturur (Pydantic dogrulama, det 1–10) ? 201 |
| GET | /icerikler?platform=&limit= | Içerikleri listeler, platforma göre filtreler |
| GET | /icerikler/{id} | Tek içerik, yoksa 404 |
| POST | /yukle | Dosya yükler, SHA-256 hash ile metadata'yi Postgres'e yazar. Ayni dosya tekrar gelirse 409 |
| GET | /dosyalar | Yüklenen dosyalarin listesi |

Swagger arayüzü: http://127.0.0.1:8000/docs

---

## Kurulum

Gereksinimler: Python 3.12, [uv](https://docs.astral.sh/uv/), bir [Neon](https://neon.com) projesi.

`powershell
git clone https://github.com/OmerCanInan/content-creator.git
cd content-creator
uv sync
`

Proje kökünde bir .env dosyasi olustur (GitHub'a gitmez):

`
DATABASE_URL=postgresql://kullanici:sifre@host/neondb?sslmode=require
`

Neon SQL Editor'de tablolari olustur:

`sql
CREATE TABLE icerikler (
    id         SERIAL PRIMARY KEY,
    baslik     TEXT NOT NULL,
    platform   TEXT NOT NULL,
    adet       INTEGER NOT NULL DEFAULT 1 CHECK (adet BETWEEN 1 AND 10),
    olusturma  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE dosyalar (
    id         SERIAL PRIMARY KEY,
    ad         TEXT NOT NULL,
    tur        TEXT,
    boyut      INTEGER NOT NULL,
    hash       TEXT NOT NULL UNIQUE,
    yuklenme   TIMESTAMPTZ NOT NULL DEFAULT now()
);
`

## Çalistirma

`powershell
uv run fastapi dev dersler/app.py      # API sunucusu
uv run dersler/istemci.py              # API'ye httpx ile örnek istekler (ikinci terminalde)
`

---

## Klasör yapisi

`
content-creator/
+-- pyproject.toml, uv.lock     # bagimliliklar
+-- main.py
+-- dersler/
¦   +-- api_deneme.py           # Ders 1: httpx, retry/backoff, GitHub API ile repo okuma
¦   +-- async_deneme.py         # Ders 2: async/await, gather, AsyncClient, Semaphore
¦   +-- semaphore_deneme.py     # Ders 2: eszamanlilik siniri denemesi
¦   +-- async_github.py         # Ders 2: GitHub dosyalarini paralel indirme (taslak)
¦   +-- app.py                  # Ders 3–4: FastAPI + Neon
¦   +-- istemci.py              # Ders 3: kendi API'ye istek atan istemci
¦   +-- db_deneme.py            # Ders 4: SQLAlchemy ile ilk baglanti
+-- veri/                       # yerel veriler (GitHub'a gitmez)
`

---

## Teknolojiler

| Alan | Kullanilan |
|---|---|
| Dil, paket yönetimi | Python 3.12, uv |
| HTTP istemcisi | httpx (senkron + async) |
| Backend | FastAPI, Pydantic, Uvicorn |
| Veritabani | PostgreSQL (Neon), SQLAlchemy, psycopg |
| Planlanan | pgvector, Gemini API, Ollama, Cloudflare R2 + Workers AI, GitHub Actions, Docker, Streamlit |

---

## Yol haritasi

**Faz 1: Egitim**
- [x] **H1:** Ortam, Python temelleri, Git/GitHub. Mini proje: klasör tarayici
- [ ] **H2:** HTTP, async, FastAPI, PostgreSQL, nesne depolama. Kapi: Swagger'dan yükle, DB'de gör *(R2 adimi kaldi)*
- [ ] **H3:** LLM, Gemini + Ollama, embedding, pgvector, RAG. Kapi: 20 soruda =16 dogru ve kaynakli
- [ ] **H4:** Vision, görsel üretim, LoRA/QLoRA, TTS/ffmpeg
- [ ] **H5:** Ajanlar, MCP, GitHub Actions cron, Docker, pytest, eval, Streamlit, güvenlik

**Faz 2: Production**
- [ ] **H6–H10:** Kaynak alimi ? bilgi tabani ve stil profili ? üretim motoru ? otonomi ve Telegram onayi ? sertlestirme. Kapi: art arda 2 hafta sifir müdahale

---

## Notlar

- .env ve eri/ asla commit edilmez.
- SQL sorgulari her zaman :parametre yer tutuculariyla yazilir (SQL injection korumasi).
- Ham dosyalar dis servislere gönderilmez. Gemini'ye sadece özetler gider.
