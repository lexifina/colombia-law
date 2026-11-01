"""Verifier reading for repeals the page dates in a marker with a comma, '<Artículo derogado, a partir del 4 de agosto de
2023, por el artículo 48 Lit. b) de la Ley 2126 de 2021>' or '<Parágrafo derogado, a partir del ..., por ...>', over words
it still prints (CIA art. 84, Ley 294 de 1996 art. 30; ../fix_ley2126_term.py), and the variants '<Artículo derogado el a
partir del 31 de diciembre de 2019 por el artículo 336 de la Ley 1955 de 2019>' (Ley 1608 de 2013 art. 7, batch 74) and
without the comma. Once the day has passed the article is
not in force today, or the paragraph's line is not part of today's text.

install(V, retrieved): wraps V.today (V = phase2/verify_phase2 as a batch verifier configures it).
"""
import re

MONTHS = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre "
                                         "diciembre".split())}
MARK = re.compile(r"<(Artículo|Parágrafo) derogado(?:,| el)? a partir del (\d{1,2}) de (\w+) de (\d{4}),? por [^<>]*>")


def install(V, retrieved: str) -> None:
    today = V.today

    def today_dated(name):
        out = today(name)
        for u in V.P.doc_units(name)[1:]:
            num = V.E.label_num(u["label"] or "")
            if not num:
                continue
            key = V.E.unit_key(num)[0]
            for k, it in enumerate([it for it in u["items"] if it[0] == "p"]):
                m = MARK.search(V.E.plain(it[1]))
                if not m:
                    continue
                day = f"{int(m.group(4)):04d}-{MONTHS[m.group(3).lower()]:02d}-{int(m.group(2)):02d}"
                if day > retrieved:
                    continue
                if m.group(1) == "Artículo" and k == 0:
                    out[key] = []
                elif m.group(1) == "Parágrafo" and out.get(key):
                    line = V.E.tidy(V.E.to_text(it[1]))
                    if out[key].count(line) != 1:
                        raise SystemExit(f"dated_repeal: {name} {key}: paragraph line not found once")
                    out[key] = [x for x in out[key] if x != line]
        return out

    V.today = today_dated
