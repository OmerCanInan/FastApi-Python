# AI Content Creator

Yüklediğim dosya, proje ve fotoğraflardan öğrenip **her hafta kendi kendine içerik paketi üreten** bir sistem.
Bütçe sıfır: ücretsiz katmanlar, açık kaynak modeller ve kendi donanımım.

> **Durum:** Faz 1 (eğitim) · Hafta 2 tamamlandı, Hafta 3 (LLM + RAG) başlıyor.

---

## Hedef mimari

```
Kaynaklar (PDF, repo, fotoğraf)
   │  dizüstü: bge-m3 embedding, Florence-2 / Qwen2.5-VL (4-bit)
   ▼
Neon (Postgres + pgvector)  ◄──►  FastAPI backend  ◄──  Streamlit panel / Telegram onayı
   ▲                                   │
   │                                   ▼
GitHub Actions (haftalık cron) ──► Gemini (metin) · Cloudflare Workers AI (görsel) · S3 uyumlu depo (dosyalar)
```

Kişisel model üç katmanlı, sıfırdan eğitim yok:
**RAG** (bilgi) → **stil profili + few-shot** (ses) → yeterli veri birikince **LoRA** (stil).

---

## Şu an çalışan kısım

FastAPI + Neon + S3 uyumlu dosya deposu üzerinde içerik kaydı ve dosya yükleme yapan bir API.

| Metot | Endpoint | Ne yapar |
|---|---|---|
| `GET` | `/` | Sağlık kontrolü |
| `POST` | `/icerikler` | İçerik oluşturur (Pydantic doğrulama, `adet` 1–10, `durum` = `taslak`) → `201` |
| `GET` | `/icerikler?platform=&limit=` | İçerikleri listeler, platforma göre filtreler |
| `GET` | `/icerikler/{id}` | Tek içerik, yoksa `404` |
| `POST` | `/yukle` | Dosyayı depoya, metadata'yı Postgres'e yazar (tek transaction). Aynı hash tekrar gelirse `409` |
| `GET` | `/dosyalar` | Yüklenen dosyaların listesi |
| `GET` | `/dosyalar/{id}/link?sure=` | Dosya için süreli imzalı link (60–3600 sn) |

Swagger arayüzü: `http://127.0.0.1:8000/docs`

---

## Kurulum

Gereksinimler: Python 3.12, [uv](https://docs.astral.sh/uv/), bir [Neon](https://neon.com) projesi, S3 uyumlu bir bucket.

```powershell
git clone https://github.com/OmerCanInan/FastApi-Python.git
cd FastApi-Python
uv sync
```

Proje kökünde bir `.env` dosyası oluştur (GitHub'a gitmez):

```
DATABASE_URL=postgresql://kullanici:sifre@host/neondb?sslmode=require
S3_ENDPOINT=https://depo-adresi
S3_REGION=bolge
S3_BUCKET=bucket-adi
S3_ACCESS_KEY=erisim-anahtari
S3_SECRET_KEY=gizli-anahtar
```

Tabloları Alembic ile oluştur:

```powershell
uv run alembic upgrade head
```

---

## Çalıştırma

```powershell
uv run fastapi dev src/content_creator/main.py   # API sunucusu → http://127.0.0.1:8000/docs
```

Şema değişikliği (SQL Editor'de elle `CREATE` / `ALTER` yapılmaz):

```powershell
uv run alembic revision -m "aciklama"   # yeni migration dosyası
uv run alembic upgrade head             # DB'yi son sürüme taşı
uv run alembic downgrade -1             # bir adım geri al
uv run alembic current                  # DB hangi sürümde
uv run alembic history                  # migration zinciri
```

---

## Klasör yapısı

```
FastApi-Python/
├── pyproject.toml, uv.lock          # bağımlılıklar
├── alembic.ini                      # Alembic ayarları (bağlantı adresi .env'den gelir)
├── migrations/
│   ├── env.py                       # DB_URL'i content_creator.db'den alır
│   └── versions/                    # şema değişiklikleri (baseline, add durum, ...)
├── src/content_creator/
│   ├── main.py                      # FastAPI app, router'ları birleştirir
│   ├── db.py                        # SQLAlchemy engine (Neon)
│   ├── depo.py                      # boto3 istemcisi (S3 uyumlu depo)
│   ├── modeller.py                  # Pydantic şemaları
│   └── routers/
│       ├── icerikler.py             # /icerikler
│       └── dosyalar.py              # /yukle, /dosyalar, /link
└── veri/                            # yerel veriler (GitHub'a gitmez)
```

Bağımlılık yönü tek taraflı: `main` → `routers` → `db` / `depo` / `modeller`. Alttaki modüller üsttekileri import etmez.

---

## Teknolojiler

| Alan | Kullanılan |
|---|---|
| Dil, paket yönetimi | Python 3.12, uv |
| HTTP istemcisi | httpx (senkron + async) |
| Backend | FastAPI, Pydantic, Uvicorn |
| Veritabanı | PostgreSQL (Neon), SQLAlchemy Core, psycopg, Alembic |
| Dosya deposu | S3 uyumlu depo, boto3, presigned URL |
| Planlanan | pgvector, Gemini API, Ollama, Cloudflare Workers AI, GitHub Actions, Docker, Streamlit |

---

## Yol haritası

**Faz 1: Eğitim**
- [x] **H1:** Ortam, Python temelleri, Git/GitHub. Mini proje: klasör tarayıcı
- [x] **H2:** HTTP, async, FastAPI, PostgreSQL, nesne depolama, Alembic. Kapı: Swagger'dan yükle, DB'de gör, linkle aç
- [ ] **H3:** LLM, Gemini + Ollama, embedding, pgvector, RAG. Kapı: 20 soruda ≥16 doğru ve kaynaklı
- [ ] **H4:** Vision, görsel üretim, LoRA/QLoRA, TTS/ffmpeg
- [ ] **H5:** Ajanlar, MCP, GitHub Actions cron, Docker, pytest, eval, Streamlit, güvenlik

**Faz 2: Production**
- [ ] **H6–H10:** Kaynak alımı → bilgi tabanı ve stil profili → üretim motoru → otonomi ve Telegram onayı → sertleştirme. Kapı: art arda 2 hafta sıfır müdahale

---

## Notlar

- `.env` ve `veri/` asla commit edilmez.
- SQL sorguları her zaman `:parametre` yer tutucularıyla yazılır (SQL injection koruması).
- Şema değişiklikleri sadece Alembic migration'ı ile yapılır; migration ve ilgili kod aynı commit'e girer.
- Ham dosyalar dış servislere gönderilmez. Gemini'ye sadece özetler gider.
- Commit mesajları İngilizce ve Conventional Commits formatında (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
