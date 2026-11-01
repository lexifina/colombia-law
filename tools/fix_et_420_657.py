"""Estatuto Tributario arts. 420 and 657 (95-batch5): their 1989-2016 history rebuilt from the page's boxes (2026-11-01).

Both articles' 'Legislación Anterior' boxes number their earlier texts ('1. Texto original del Decreto 624 de 1989:',
'2 Texto original del Estatuto Tributario, modificado por la Ley 49 de 1990:', ...). The engine reads only headings that
start with 'Texto', so it took the whole box, every earlier text one after the other, as the 1989 text and kept it until
Ley 1819 de 2016. This script gives each unit one version per amending act instead, from the box texts, every changed
line checked word for word against the amending act's own article (the act's basedoc page; Ley 49 de 1990, which the
basedoc does not hold, from the same compilation's Colpensiones copy), on the day the part already gives that act:

Art. 420: original text (1989-05-30); Ley 6 de 1992 art. 25 (literal b); Ley 223 de 1995 art. 176 (parágrafo 2o); Ley
383 de 1997 art. 33 (parágrafos 3o and 4o); Ley 488 de 1998 art. 53 (numeral 3 heading, its literal a, literal g); Ley
633 de 2000 arts. 28, 29 and 134 (parágrafo 5o, literal h, the phrase 'Lo anterior no se aplica a los servicios de radio
y de televisión' out); Ley 788 de 2002 art. 115 (literal d); Sentencia C-1147 de 2003 (art. 115 INEXEQUIBLE: literal d
out, 2003-12-02); Ley 863 de 2003 art. 62 (literal d again, its own wording); Ley 1111 de 2006 arts. 51 and 78 (the
minimum wages of literal d in UVT, 20 and 290, from art. 51's table; inciso 2 of parágrafo 5o repealed); Decreto 127 de
2010 art. 3 and Ley 1393 de 2010 art. 3 (inciso 4 of literal d); Ley 1739 de 2014 art. 64 (inciso 3 of literal d).
The box's last earlier text puts Ley 1739's words in place of inciso 2 ('El impuesto se causa ...') and keeps the old
inciso 3; the act names inciso 3, so inciso 2 stays and inciso 3 changes. The boxes from Ley 863 on leave out the
original parágrafo (activos fijos); no act or note repeals it, so it stays until Ley 1819 rewrote the article.

Art. 657: original text (1989-05-30); Ley 49 de 1990 art. 42 (literal b); Ley 6 de 1992 art. 56 (literal a, inciso
4); Ley 223 de 1995 art. 47 (literal a, inciso 4); Ley 488 de 1998 arts. 74 and 75 (literal a, inciso 2); Ley 633 de
2000 art. 41 (literal c); Ley 863 de 2003 art. 25 (literals d, e, f); Ley 1111 de 2006 art. 78 (literal d repealed;
the box's last earlier text still prints it). Sentencia C-616 de 2002's conditional ruling on literal c keeps its
credit (it changed no words).

Idempotent: the unit's versions between 1989-05-30 and 2016-12-29 are recomputed from the same stages each run.
RE-RUN ORDER: after any re-parse of batch 5, after fix_dated_struck.py and before fix_box_text.py.

Usage: python -X utf8 fix_et_420_657.py [--to DIR]
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
_argv, sys.argv = sys.argv[1:], sys.argv[:1]
sys.path.insert(0, HERE)
import fix_dated_struck as FD  # noqa: E402

E = FD.E
PART = "95-batch5.json"
SLUG = "estatuto-tributario"
END = "2016-12-29"  # Ley 1819 de 2016: the part's own history from here on is kept
TAG = "Estatuto Tributario arts. 420 and 657 (2026-11-01):"
WORD = re.compile(r"[0-9a-záéíóúñü]+")
C1147 = {"label": "Sentencia C-1147 de 2003", "title": "Corte Constitucional, Sentencia C-1147 de 2003", "kind": "court",
         "enacted": "2003-12-02", "published": None,
         "url": "http://www.secretariasenado.gov.co/senado/basedoc/c-1147_2003.html", "temporary_until": None,
         "restores": None, "note": None}
COLP_49 = "https://normativa.colpensiones.gov.co/colpens/docs/ley_0049_1990.htm"


class Stop(Exception):
    pass


def words(t):
    """Words without accents: the boxes and the acts' pages differ in accents ('PARAGRAFO' / 'PARÁGRAFO')."""
    t = unicodedata.normalize("NFD", t.lower())
    return set(WORD.findall("".join(c for c in t if not unicodedata.combining(c))))


# ---------------------------------------------------------------- sources
def boxes(anchor):
    """The unit's earlier texts, oldest first: [(heading, [lines])] (numbered and plain 'Texto ...' headings)."""
    u = next(x for x in E.doc_units("estatuto_tributario")[1:] if x["name"] == anchor)
    out = []
    for it in u["items"]:
        if it[0] != "box" or it[1] != "Legislación Anterior":
            continue
        cur = None
        for ph in E.box_paras(it[2]):
            t = E.tidy(E.to_text(ph))
            if re.match(r"(\d+\.?\s+)?Texto ", t) and re.search(r"<span class='b_aj'>", ph):
                cur = [t, []]
                out.append(cur)
            elif cur is not None and t.strip():
                cur[1].append(ph)
    res = []
    for head, paras in reversed(out):
        res.append((head, E.block_text(paras, E.is_full(paras))))
    return res


def article(page, num):
    """An amending act's article: its paragraphs and note boxes as plain text (struck words kept)."""
    u = next(x for x in E.doc_units(page) if x["name"] == num)
    return " ".join(E.tidy(E.to_text(it[1])) if it[0] == "p" else E.plain(it[2]) for it in u["items"])


def page_text(page):
    return " ".join(E.plain(E.read(E.BASE + p + ".html") or "") for p in E.pages(page))


def ley49_art42():
    h = E.read(COLP_49)
    if not h:
        raise Stop("Ley 49 de 1990 page not available")
    t = re.sub(r"\s+", " ", E.plain(h))
    i, j = t.find("ARTICULO 42. FACTURACION"), t.find("ARTICULO 43.")
    if i < 0 or j < i:
        raise Stop("Ley 49 de 1990 art. 42 not found")
    return t[i:j]


# ---------------------------------------------------------------- stages
def find(lines, prefix):
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise Stop(f"{len(hits)} lines start with {prefix!r}")
    return hits[0]


def line_of(block, prefix):
    return block[find(block, prefix)]


def stages_420():
    B = boxes("420")
    heads = [h for h, _ in B]
    if len(B) != 10 or not heads[0].startswith("1. Texto original") or "1918 de 2016" not in heads[8]:
        raise Stop(f"art. 420 boxes changed: {heads}")
    b = [lines for _, lines in B]
    s = list(b[0])                                   # original text
    st = [("1989-05-30", None, list(s), None)]

    def stage(day, law, src):
        st.append((day, law, list(s), src))

    s[find(s, "b) La prestación")] = line_of(b[1], "b. La prestación")
    stage("1992-06-30", "ley-6-1992", article("ley_0006_1992", "25"))
    s.append(line_of(b[1], "PARAGRAFO 2o."))
    stage("1995-12-22", "ley-223-1995", article("ley_0223_1995", "176"))
    i, j = find(b[1], "PARAGRAFO 3o."), find(b[1], "PARAGRAFO 4o.")
    par3 = b[1][i:j + 1]
    par3[par3.index(line_of(par3, "Lo previsto por el numeral tercero"))] = line_of(b[2], "Lo previsto por el numeral tercero")
    s += par3                                        # the closing quote mark of the act's quoted text left out
    stage("1997-07-14", "ley-383-1997", article("ley_0383_1997", "33"))
    s[find(s, "3. Los siguientes servicios")] = line_of(b[2], "3. Los siguientes servicios")
    s[find(s, "a) Los servicios de arrendamiento")] = line_of(b[2], "a. Las licencias")
    s.insert(find(s, "Lo previsto por el numeral tercero"), line_of(b[2], "g) Los servicios de conexión"))
    stage("1998-12-28", "ley-488-1998", article("ley_0488_1998", "53"))
    s[find(s, "g) Los servicios de conexión")] = line_of(b[3], "g) Los servicios de conexión")
    s.insert(find(s, "Lo previsto por el numeral tercero"), line_of(b[3], "h) El servicio de televisión"))
    k = find(b[3], "PARAGRAFO 5o.")
    s += b[3][k:k + 2]
    if not s[-1].startswith("La base gravable del impuesto a las ventas sobre los cigarrillos"):
        raise Stop("art. 420 parágrafo 5o inciso 2 not where expected")
    stage("2000-12-29", "ley-633-2000", " ".join(article("ley_0633_2000", n) for n in ("28", "29", "134")))
    d788 = b[1][find(b[1], "d) Impuesto sobre las ventas"):find(b[1], "PARAGRAFO.")]
    if len(d788) != 6:
        raise Stop("art. 420 Ley 788 literal d) not six lines")
    at = find(s, "PARAGRAFO.")
    s[at:at] = d788
    stage("2002-12-27", "ley-788-2002", article("ley_0788_2002", "115"))
    del s[at:at + 6]
    stage("2003-12-02", "c-1147-03", None)
    d863 = b[4][find(b[4], "d) Impuesto sobre las Ventas"):find(b[4], "PARAGRAFO 2o.")]
    if len(d863) != 6:
        raise Stop("art. 420 Ley 863 literal d) not six lines")
    s[at:at] = d863
    stage("2003-12-29", "ley-863-2003", article("ley_0863_2003", "62"))
    s[find(s, "La base gravable estará constituida")] = line_of(b[5], "La base gravable estará constituida")
    del s[find(s, "La base gravable del impuesto a las ventas sobre los cigarrillos")]
    stage("2006-12-27", "ley-1111-2006", article("ley_0863_2003", "62") + " " + article("ley_1111_2006", "78")
          + " UVT 20 290")
    s[find(s, "La tarifa del impuesto sobre las ventas en los juegos")] = line_of(b[6], "A partir del 1o de febrero")
    stage("2010-01-21", "dec-127-2010", article("decreto_0127_2010", "3"))
    s[find(s, "A partir del 1o de febrero")] = line_of(b[7], "En los juegos de suerte y azar se aplicará")
    stage("2010-07-12", "ley-1393-2010", article("ley_1393_2010", "3"))
    s[find(s, "La base gravable estará constituida")] = line_of(b[8], "La base gravable estará constituida por el valor de la apuesta, del documento, formulario, boleta, billete o instrumento que da derecho a participar en el juego. En el caso de los juegos localizados tales como las maquinitas o tragamonedas, la base gravable mensual")
    stage("2014-12-23", "ley-1739-2014", article("ley_1739_2014", "64"))
    # Ley 1111 art. 51's table gives 1 -> 20 UVT and 14 -> 290 UVT for 'ART. 420 LITERAL d)'.
    t = re.sub(r"\s+", "", page_text("ley_1111_2006"))
    if "ART.420LITERALd)E.T.11PRIMERVALOR1408.0002012SEGUNDOVALOR145.712.000290" not in t:
        raise Stop("Ley 1111 art. 51 table row for art. 420 not found")
    if "el inciso 2o del parágrafo 5o del artículo 420" not in article("ley_1111_2006", "78"):
        raise Stop("Ley 1111 art. 78 does not repeal inciso 2 of parágrafo 5o of art. 420")
    if "lo anterior no se aplica a los servicios de radio y televisión" not in article("ley_0633_2000", "134"):
        raise Stop("Ley 633 art. 134 phrase not found")
    return st


def stages_657():
    B = boxes("657")
    heads = [h for h, _ in B]
    if len(B) != 9 or not heads[0].startswith("1 Texto original") or "ley 1819 de 2016" not in heads[6]:
        raise Stop(f"art. 657 boxes changed: {heads}")
    b = [lines for _, lines in B]
    s = list(b[0])
    st = [("1989-05-30", None, list(s), None)]

    def stage(day, law, src):
        st.append((day, law, list(s), src))

    s[find(s, "b) ")] = line_of(b[1], "b) ")
    stage("1991-02-28", "ley-49-1990", ley49_art42())
    s[find(s, "a) ")] = line_of(b[2], "a) ")
    s[find(s, "En caso de reincidencia")] = line_of(b[2], "Una vez aplicada")
    stage("1992-06-30", "ley-6-1992", article("ley_0006_1992", "56"))
    s[find(s, "a) ")] = line_of(b[3], "a) ")
    s[find(s, "Una vez aplicada")] = line_of(b[3], "Una vez aplicada")
    stage("1995-12-22", "ley-223-1995", article("ley_0223_1995", "47"))
    s[find(s, "a) ")] = line_of(b[4], "a) ")
    s[find(s, "La sanción a que se refiere el presente artículo, se aplicará")] = line_of(b[4], "La sanción a que se refiere el presente artículo, se aplicará")
    stage("1998-12-28", "ley-488-1998", article("ley_0488_1998", "74") + " " + article("ley_0488_1998", "75"))
    s.insert(find(s, "b) ") + 1, line_of(b[5], "c) "))
    stage("2000-12-29", "ley-633-2000", article("ley_0633_2000", "41"))
    at = find(s, "c) ") + 1
    s[at:at] = [line_of(b[6], x) for x in ("d) ", "e) ", "f) ")]
    stage("2003-12-29", "ley-863-2003", article("ley_0863_2003", "25"))
    del s[find(s, "d) ")]
    stage("2006-12-27", "ley-1111-2006", None)
    if "el literal d) del artículo 657" not in article("ley_1111_2006", "78"):
        raise Stop("Ley 1111 art. 78 does not repeal literal d) of art. 657")
    if [l for l in b[6] if not l.startswith("d) ")] != s:
        raise Stop("art. 657: last stage is not the box's 'vigente antes de Ley 1819' text less literal d)")
    return st


def check_words(st, label):
    """Every word of a line a stage adds or changes stands in the amending act's article (src)."""
    for (d0, _, prev, _), (day, law, cur, src) in zip(st, st[1:]):
        new = [l for l in cur if l not in prev]
        if src is None:
            if new:
                raise Stop(f"{label} {day}: lines added with no source")
            continue
        # a line that only loses words (a phrase repealed) needs no source beyond the line it was
        new = [l for l in new if not any(words(l) <= words(p) for p in prev)]
        miss = set().union(*[words(l) for l in new]) - words(src) if new else set()
        if miss:
            raise Stop(f"{label} {day} {law}: words not in the act: {sorted(miss)}")


# ---------------------------------------------------------------- patch
def patch(part, act, key, st, log):
    vs = act["versions"]
    days = [v["from"] for v in vs]
    if days[0] != st[0][0] or END not in days:
        raise Stop("version days not as expected")
    by_day = {day: (law, lines) for day, law, lines, _ in st}
    for day in by_day:
        if day not in days:
            raise Stop(f"{key}: no version on {day}")
    unit = dict(vs[0]["units"][key])
    head = unit["text"].split("\n", 1)[0]

    def text(lines):
        return head + "\n" + "\n".join(lines) + "\n"
    before = [t for _, t in FD.states(act, key)]
    end = days.index(END)
    for i in range(end):
        v = vs[i]
        law, lines = by_day.get(v["from"], (None, None))
        cr = v.get("credits", {})
        if lines is not None:
            u = dict(unit, text=text(lines))
            if i == 0:
                v["units"][key] = u
            else:
                v.setdefault("changes", {})[key] = u
                cr[key] = [law]
        elif i > 0:
            (v.get("changes") or {}).pop(key, None)
            keep = [c for c in cr.get(key, []) if c == "c-616-02" and key == "art-0657"]
            if keep:
                cr[key] = keep
            else:
                cr.pop(key, None)
    for i in range(1, end):  # a change entry equal to the state before it is dropped (nothing to commit)
        v = vs[i]
        if key in (v.get("changes") or {}):
            prev = FD.states(act, key)[i - 1][1]
            if v["changes"][key]["text"] == prev:
                raise Stop(f"{key} {v['from']}: stage equals the text before it")
    after = [t for _, t in FD.states(act, key)]
    if after[end:] != before[end:]:
        raise Stop(f"{key}: versions from {END} on would change")
    if after != before:
        log.append(key)
    return after != before


def main(argv):
    out_dir = None
    if "--to" in argv:
        out_dir = argv[argv.index("--to") + 1]
        os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "corpus.d", PART)
    if out_dir and os.path.exists(os.path.join(out_dir, PART)):
        src = os.path.join(out_dir, PART)
    part = json.load(open(src, encoding="utf-8"))
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    s420, s657 = stages_420(), stages_657()
    check_words(s420, "art. 420")
    check_words(s657, "art. 657")
    log = []
    patch(part, act, "art-0420", s420, log)
    patch(part, act, "art-0657", s657, log)
    changed = bool(log)
    if part["laws"].get("c-1147-03") != C1147:
        if "c-1147-03" in part["laws"]:
            raise Stop("c-1147-03 entry differs from the shared one")
        part["laws"]["c-1147-03"] = C1147
        changed = True
    dec = (TAG + " the 'Legislación Anterior' boxes of these two articles number their earlier texts ('1. Texto "
           "original ...', '2 Texto original ..., modificado por la Ley 49 de 1990:'), which the engine did not read as "
           "headings, so the whole box had stood as the 1989 text until Ley 1819 de 2016. Their 1989-2016 history is "
           "rebuilt from those boxes, one version per amending act on the day this part gives it, every changed line "
           "checked word for word against the act's own article: art. 420: Ley 6 de 1992 art. 25, Ley 223 de 1995 art. "
           "176, Ley 383 de 1997 art. 33, Ley 488 de 1998 art. 53, Ley 633 de 2000 arts. 28, 29 and 134, Ley 788 de "
           "2002 art. 115 (literal d), Sentencia C-1147 de 2003 (that article INEXEQUIBLE, literal d out from "
           "2003-12-02), Ley 863 de 2003 art. 62 (literal d again), Ley 1111 de 2006 arts. 51 (values in UVT, from its "
           "table) and 78 (inciso 2 of parágrafo 5o repealed), Decreto 127 de 2010 art. 3, Ley 1393 de 2010 art. 3, "
           "Ley 1739 de 2014 art. 64 (the act replaces inciso 3 of literal d, the base; the box's last earlier text "
           "replaced inciso 2 instead, and the act is followed); the original parágrafo (activos fijos), which the "
           "boxes from Ley 863 on leave out and no act repeals, stays until Ley 1819; art. 657: Ley 49 de 1990 art. 42 "
           "(the compilation's Colpensiones copy, as the basedoc does not hold the act), Ley 6 de 1992 art. 56, Ley 223 "
           "de 1995 art. 47, Ley 488 de 1998 arts. 74 and 75, Ley 633 de 2000 art. 41, Ley 863 de 2003 art. 25, Ley "
           "1111 de 2006 art. 78 (literal d repealed; the box's last earlier text still prints it).")
    if dec not in part["decisions"]:
        part["decisions"] = [d for d in part["decisions"] if not d.startswith(TAG)] + [dec]
        changed = True
    print("changed units:", log or "none", "| part changed:", changed)
    if changed:
        path = os.path.join(out_dir, PART) if out_dir else os.path.join(HERE, "corpus.d", PART)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)


if __name__ == "__main__":
    try:
        main(_argv)
    except Stop as e:
        sys.exit(f"STOP: {e}")
