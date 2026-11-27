import ast

AYIRICILAR = ("\n\n", "\n", ". ", " ")


def markdown_parcala(metin: str) -> list[str]:
    parcalar = []
    mevcut = []
    kod_blogunda = False
    for satir in metin.splitlines():
        if satir.startswith("```"):
            kod_blogunda = not kod_blogunda
        if satir.startswith("#") and mevcut and not kod_blogunda:
            parcalar.append("\n".join(mevcut).strip())
            mevcut = []
        mevcut.append(satir)
    if mevcut:
        parcalar.append("\n".join(mevcut).strip())
    return [p for p in parcalar if p]


def boyuta_bol(metin: str, sinir: int = 1200,
               ayiricilar: tuple[str, ...] = AYIRICILAR) -> list[str]:
    if len(metin) <= sinir:
        return [metin]
    if not ayiricilar:
        return [metin[i:i + sinir] for i in range(0, len(metin), sinir)]

    ayirici = ayiricilar[0]
    sonuc = []
    mevcut = ""
    for parca in metin.split(ayirici):
        aday = parca if not mevcut else mevcut + ayirici + parca
        if len(aday) <= sinir:
            mevcut = aday
            continue
        if mevcut:
            sonuc.append(mevcut)
        if len(parca) <= sinir:
            mevcut = parca
        else:
            sonuc.extend(boyuta_bol(parca, sinir, ayiricilar[1:]))
            mevcut = ""
    if mevcut:
        sonuc.append(mevcut)
    return sonuc


def metin_parcala(metin: str, sinir: int = 1200) -> list[str]:
    sonuc = []
    for bolum in markdown_parcala(metin):
        sonuc.extend(boyuta_bol(bolum, sinir))
    return sonuc


TANIMLAR = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def kod_parcala(kod: str) -> list[tuple[str,str]]:
    agac = ast.parse(kod)
    satirlar = kod.splitlines()
    ust_kisim = []
    parcalar = []
    for dugum in agac.body:
        bas = dugum.lineno
        if isinstance(dugum, TANIMLAR) and dugum.decorator_list:
            bas = dugum.decorator_list[0].lineno
        parca = "\n".join(satirlar[bas - 1:dugum.end_lineno])
        if isinstance(dugum, TANIMLAR):
            parcalar.append((dugum.name, parca))
        else:
            ust_kisim.append(parca)
    if ust_kisim:
        parcalar.insert(0, ("_ust", "\n".join(ust_kisim)))
    return parcalar
