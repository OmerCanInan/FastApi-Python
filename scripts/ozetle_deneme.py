from pathlib import Path

from content_creator.ozetle import dosya_ozetle

kaynak = "src/content_creator/llm.py"
ozet = dosya_ozetle(kaynak, Path(kaynak).read_text(encoding="utf-8"))

print("GENEL:", ozet.genel)
for f in ozet.fonksiyonlar:
    print(f"\n{f.ad}:\n  {f.aciklama}")