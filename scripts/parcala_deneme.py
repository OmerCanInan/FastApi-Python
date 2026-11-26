from pathlib import Path

from content_creator.parcala import markdown_parcala

metin = Path("README.md").read_text(encoding="utf-8")
parcalar = markdown_parcala(metin)

print(len(parcalar), "parça")
for i, p in enumerate(parcalar):
    ilk_satir = p.splitlines()[0]
    print(f"{i:2} | {len(p):5} karakter | {ilk_satir}")