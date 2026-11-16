# AI Content Creator

Yüklediğim dosya, proje ve fotoğraflardan öğrenip **her hafta kendi kendine içerik paketi üreten** bir sistem.
Bütçe sıfır: ücretsiz katmanlar, açık kaynak modeller ve kendi donanımım.

> **Durum:** Faz 1 (eğitim) · Hafta 2 tamamlanıyor. Bu repo şu an hem öğrenme defteri (`dersler/`) hem de projenin ilk backend'i.

---

## Hedef mimari

```
Kaynaklar (PDF, repo, fotoğraf)
   │  dizüstü: bge-m3 embedding, Florence-2 / Qwen2.5-VL (4-bit)
   ▼
Neon (Postgres + pgvector)  ◄──►  FastAPI backend  ◄──  Streamlit panel / Telegram onayı
   ▲                                   │
   │                                   ▼
GitHub Actions (haftalık cron) ──► Gemini (metin) · Cloudflare Workers AI (görsel) · R2 (dosyalar)
```

Kişisel model üç katmanlı, sıfırdan eğitim yok:
**RAG** (bilgi) → **stil profili + few-shot** (ses) → yeterli veri birikince **LoRA** (stil).

---

## Şu an çalışan kısım

FastAPI + Neon üzerinde, içerik kaydı ve dosya yükleme yapan bir API.

| Metot | Endpoint | Ne yapar |
|---|---|---|
| `GET` | `/` | Sağlık kontrolü |
| `POST` | `/icerikler` | İçerik oluşturur (Pydantic doğrulama, `adet` 1–10) → `201` |
| `GET` | `/icerikler?platform=&limit=` | İçerikleri listeler, platforma göre filtreler |
| `GET` | `/icerikler/{id}` | Tek içerik, yoksa `404` |
| `POST` | `/yukle` | Dosya yükler, SHA-256 hash ile metadata'yı Postgres'e yazar. Aynı dosya tekrar gelirse `409` |
| `GET` | `/dosyalar` | Yüklenen dosyaların listesi |

Swagger arayüzü: `http://127.0.0.1:8000/docs`

---

## Kurulum

Gereksinimler: Python 3.12, [uv](https://docs.astral.sh/uv/), bir [Neon](https://neon.com) projesi.

```powershell
git clone https://github.com/OmerCanInan/content-creator.git
cd content-creator
uv sync
```

Proje kökünde bir `.env` dosyası oluştur (GitHub'a gitmez):

```
DATABASE_URL=postgresql://kullanici:sifre@host/neondb?sslmode=require
```

Neon SQL Editor'de tabloları oluştur:

```sql
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
```

## Çalıştırma

```powershell
uv run fastapi dev dersler/app.py      # API sunucusu
uv run dersler/istemci.py              # API'ye httpx ile örnek istekler (ikinci terminalde)
```

---

## Klasör yapısı

```
content-creator/
├── pyproject.toml, uv.lock     # bağımlılıklar
├── main.py
├── dersler/
│   ├── api_deneme.py           # Ders 1: httpx, retry/backoff, GitHub API ile repo okuma
│   ├── async_deneme.py         # Ders 2: async/await, gather, AsyncClient, Semaphore
│   ├── semaphore_deneme.py     # Ders 2: eşzamanlılık sınırı denemesi
│   ├── async_github.py         # Ders 2: GitHub dosyalarını paralel indirme (taslak)
│   ├── app.py                  # Ders 3–4: FastAPI + Neon
│   ├── istemci.py              # Ders 3: kendi API'ye istek atan istemci
│   └── db_deneme.py            # Ders 4: SQLAlchemy ile ilk bağlantı
└── veri/                       # yerel veriler (GitHub'a gitmez)
```

---

## Teknolojiler

| Alan | Kullanılan |
|---|---|
| Dil, paket yönetimi | Python 3.12, uv |
| HTTP istemcisi | httpx (senkron + async) |
| Backend | FastAPI, Pydantic, Uvicorn |
| Veritabanı | PostgreSQL (Neon), SQLAlchemy, psycopg |
| Planlanan | pgvector, Gemini API, Ollama, Cloudflare R2 + Workers AI, GitHub Actions, Docker, Streamlit |

---

## Yol haritası

**Faz 1: Eğitim**
- [x] **H1:** Ortam, Python temelleri, Git/GitHub. Mini proje: klasör tarayıcı
- [ ] **H2:** HTTP, async, FastAPI, PostgreSQL, nesne depolama. Kapı: Swagger'dan yükle, DB'de gör *(R2 adımı kaldı)*
- [ ] **H3:** LLM, Gemini + Ollama, embedding, pgvector, RAG. Kapı: 20 soruda ≥16 doğru ve kaynaklı
- [ ] **H4:** Vision, görsel üretim, LoRA/QLoRA, TTS/ffmpeg
- [ ] **H5:** Ajanlar, MCP, GitHub Actions cron, Docker, pytest, eval, Streamlit, güvenlik

**Faz 2: Production**
- [ ] **H6–H10:** Kaynak alımı → bilgi tabanı ve stil profili → üretim motoru → otonomi ve Telegram onayı → sertleştirme. Kapı: art arda 2 hafta sıfır müdahale

---

## Notlar

- `.env` ve `veri/` asla commit edilmez.
- SQL sorguları her zaman `:parametre` yer tutucularıyla yazılır (SQL injection koruması).
- Ham dosyalar dış servislere gönderilmez. Gemini'ye sadece özetler gider.
