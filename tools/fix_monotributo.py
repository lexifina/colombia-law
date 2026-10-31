"""Give the Estatuto Tributario's Libro Octavo 'Monotributo' (arts. 903 to 916, added by Ley 1819 de 2016, art. 165) its
text from 2016-12-29 until Ley 1943 de 2018 replaced it on 2018-12-28, in corpus.d/95-batch5.json, without re-parsing.

The Estatuto's page gives, for each of these articles, only the earlier-text box 'Texto adicionado por la Ley 1819 de
2016: Consultar texto original del Libro Octavo 'Monotributo' directamente en el artículo 165 Ley 1819 de 2016', so the
part had them absent between the two acts. The text is taken from that article of Ley 1819 de 2016 on its own Senado
basedoc page: each 'Artículo 9NN.' paragraph and the paragraphs after it up to the next article or chapter heading,
without the 'Artículo 9NN.' heading words. The table of art. 908 (monotributo categories) is not a paragraph and is left
out, as the engine leaves tables out everywhere. Idempotent.

Usage:  python -X utf8 fix_monotributo.py [corpus.d folder]
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import engine as E  # noqa: E402

PART, SLUG, LAW, START, END = "95-batch5.json", "estatuto-tributario", "ley-1819-2016", "2016-12-29", "2018-12-28"
BOX = "Consultar texto original del Libro Octavo"
DECISION = ("Estatuto Tributario, arts. 903 to 916 (Libro Octavo 'Monotributo', added by Ley 1819 de 2016, art. 165): the "
            "Estatuto's page refers to Ley 1819 de 2016, art. 165 for their text ('Consultar texto original del Libro Octavo "
            "Monotributo directamente en el artículo 165 Ley 1819 de 2016'); that article's text on the act's own basedoc "
            "page stands from 2016-12-29 until Ley 1943 de 2018 replaced the Libro on 2018-12-28 (art. 908's table of "
            "categories left out, as tables are everywhere) (fix_monotributo.py).")


def states(vs):
    cur, out = {}, []
    for v in vs:
        if "units" in v:
            cur = copy.deepcopy(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append(dict(cur))
    return out


def monotributo() -> dict[str, list[str]]:
    u = next((x for x in E.doc_units("ley_1819_2016") if x["name"] == "165"), None)
    if u is None:
        raise SystemExit("ley_1819_2016: art. 165 not found")
    ps = [E.tidy(E.to_text(it[1])) for it in u["items"] if it[0] == "p"]
    out, cur = {}, None
    for p in ps:
        m = re.match(r"Art[íi]culo (9\d\d)\.\s+(.*)", p)
        if m:
            cur = m.group(1)
            out[cur] = [m.group(2)]
        elif re.match(r"(CAP[ÍI]TULO|LIBRO|MONOTRIBUTO$|Disposiciones|Inscripci[óo]n, declaraci)", p) or not p:
            cur = None if p else cur
        elif cur:
            out[cur].append(p)
    if sorted(out) != [str(n) for n in range(903, 917)]:
        raise SystemExit(f"ley_1819_2016 art. 165: articles {sorted(out)}")
    return out


def main(argv):
    folder = argv[0] if argv else os.path.join(HERE, "corpus.d")
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    if DECISION in part["decisions"]:
        print(PART, "already fixed")
        return
    # the Estatuto's own page points to Ley 1819 art. 165 for every one of them
    boxes = 0
    for u in E.doc_units("estatuto_tributario"):
        n = E.label_num(u["label"] or "")
        if n and n.isdigit() and 903 <= int(n) <= 916:
            if any(BOX in E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior"):
                boxes += 1
    texts = monotributo()
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    sts = states(vs)
    last = sts[-1]
    for n, lines in texts.items():
        key = f"art-{int(n):04d}"
        label = next(s[key]["label"] for s in sts if key in s)
        kind = next(s[key]["kind"] for s in sts if key in s)
        for v, st in zip(vs, sts):
            if START <= v["from"] < END:
                if key in st:
                    raise SystemExit(f"{key} present on {v['from']}")
                st[key] = {"label": label, "kind": kind, "text": f"# {label}\n" + "".join(l + "\n" for l in lines)}
                if v["from"] == START:
                    v["credits"].setdefault(key, [LAW])
    if boxes < 12:
        raise SystemExit(f"only {boxes} articles point to Ley 1819 art. 165")
    prev = None
    for j, (v, st) in enumerate(zip(vs, sts)):
        if j == 0:
            v["units"] = st
        else:
            ch = {k: u for k, u in st.items() if prev.get(k) != u}
            ch.update({k: None for k in prev if k not in st})
            if ch:
                v["changes"] = ch
            else:
                v.pop("changes", None)
        prev = st
    if states(vs)[-1] != last:
        raise SystemExit("today's text changed")
    part["decisions"].append(DECISION)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed", len(texts), "articles;", boxes, "of them point to Ley 1819 art. 165 on the Estatuto's page")


if __name__ == "__main__":
    main(sys.argv[1:])
