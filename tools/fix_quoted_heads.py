"""Put back article text the engine had moved into titulos.md (quoted books/chapters of another code given their own
heading anchors, or an article whose heading holds a misplaced title anchor), in published parts, in place.

The words come from the page as the part's verifier reads it (with the page repair now in that batch's driver), so the
patched part and a re-parse agree. Idempotent: an article already holding the words is left alone. Each entry checks
that every version defining the article holds a prefix of the new words (the text before the lost part), and takes out
of titulos.md the heading line holding the lost words.

HEADJOIN entries (2026-10-31, second round: the parts PROGRESS.md listed as 'OPEN (same family)') are the units that
phase2/headjoin.py repairs in the drivers of 50-codes, 80-batch3, 90-batch4, 97-batch6, 99a-batch9 and 99c-batch11:
- an article missing from every version (its unit had been read as a heading: CC art. 642, CCom art. 441, CNSCC art. 5,
  Ley 5 de 1992 art. 309) goes into the act's first version, as the page prints it (the re-parse dates it so: none of
  them has a change since);
- an article's tail (blocks under heading-named anchors after it: EOSF arts. 112, 183, 193, 218, 270; Ley 715 art. 84A)
  ends every version whose text of the article is the part's last text of it (headjoin.tail_lines: the lines the
  re-parse adds there, since headjoin.install() keeps the history of the article without its tail);
- titulos.md loses the heading lines that held those words (a line starting with a tail line, or a line given), or
  gets the line the re-parse shows in its place.
The part's decision is headjoin.decision(), the sentence the re-parse writes. Idempotent; a no-op after a re-parse with
the repaired drivers.

Usage: python -X utf8 fix_quoted_heads.py [corpus.d folder]
"""
import importlib
import json
import os
import sys

C = os.path.dirname(os.path.abspath(__file__))
# (part, verifier module dir, verifier module, act slug, page, unit key, label, start of the titulos line to drop)
FIXES = [
    ("99k-batch19", "batch19", "verify_batch19", "reforma-financiera-2009", "ley_1328_2009", "art-0065", "Art. 65",
     "### CAPÍTULO XIV. SUCURSALES DE BANCOS Y COMPAÑÍAS DE SEGUROS DEL EXTERIOR. Artículo 45A."),
    ("99k-batch19", "batch19", "verify_batch19", "conglomerados-financieros", "ley_1870_2017", "art-0002", "Art. 2",
     "### o ARTÍCULO 2. CONGLOMERADO FINANCIERO."),
]


def main(argv):
    folder = argv[0] if argv else os.path.join(C, "corpus.d")
    done = []
    for part, d, mod, slug, page, key, label, tit in FIXES:
        path = os.path.join(folder, part + ".json")
        data = json.load(open(path, encoding="utf-8"))
        act = next(a for a in data["acts"] if a["slug"] == slug)
        sys.path.insert(0, os.path.join(C, d))
        V = importlib.import_module(mod).V
        new = V.today(page)[key]
        if not new:
            sys.exit(f"{page} {key}: no text on the page")
        text = "# " + label + "\n" + "\n".join(new) + "\n"
        changed = False
        for v in act["versions"]:
            for field in ("units", "changes"):
                us = v.get(field)
                if not us:
                    continue
                u = us.get(key)
                if u is not None and u["text"] != text:
                    old = u["text"].split("\n")[1:-1]
                    if new[:len(old)] != old:
                        sys.exit(f"{part} {slug} {key} {v['from']}: the old text is not a prefix of the page's")
                    us[key] = dict(u, text=text)
                    changed = True
                t = (us.get("titulos") or {}).get("text")
                if t and any(l.startswith(tit) for l in t.split("\n")):
                    us["titulos"] = dict(us["titulos"], text="".join(l + "\n" for l in t.split("\n")[:-1] if not l.startswith(tit)))
                    changed = True
        first = act["versions"][0]
        if key not in first["units"] and all(key not in (v.get("units") or {}) and key not in (v.get("changes") or {})
                                             for v in act["versions"]):
            # an article missing from every version: in the act's first version, as the page prints it (the part's
            # other articles of the same title start there too)
            first["units"] = dict(sorted({**first["units"], key: {"label": label, "kind": "art", "text": text}}.items()))
            changed = True
        if changed:
            dec = (f"{act['title']}: {label} — words the page gives after a heading anchor (a quoted chapter, or a title "
                   f"anchor misplaced inside the article's heading) had been read as headings and were missing from the "
                   f"article; they are back in it (fix_quoted_heads.py, 2026-10-31).")
            if dec not in data["decisions"]:
                data["decisions"].append(dec)
            open(path + ".tmp", "w", encoding="utf-8", newline="\n").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + chr(10))
            os.replace(path + ".tmp", path)
            done.append(f"{part} {slug} {key}")
    done += headjoin_fixes(folder)
    print("patched:", done or "none")


for _d in ("batch11", "batch10", "batch9", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    if os.path.join(C, _d) not in sys.path:
        sys.path.append(os.path.join(C, _d))
# (part, driver dir, verifier module (None: codes, read as codes/verify_today.py does), driver module, its repaired
#  doc_units, slug, page, act title, {key: "whole" | "tail"}, {start of an old titulos line: the line in its place, or None})
HEADJOIN = [
    ("50-codes", "codes", None, "parse_codes", "doc_units", "codigo-civil", "codigo_civil", "Código Civil",
     {"art-0642": "whole"}, {"### ARTÍCULO 642.. Toda corporación": None}),
    ("80-batch3", "batch3", "verify_batch3", "parse_batch3", "doc_units", "codigo-de-comercio", "codigo_comercio",
     "Código de Comercio (Decreto 410 de 1971)", {"art-0441": "whole"},
     {"### ARTÍCULO 441.. En el registro mercantil": None}),
    ("90-batch4", "batch4", "verify_batch4", "parse_batch4", "doc_units",
     "codigo-nacional-de-seguridad-y-convivencia-ciudadana", "ley_1801_2016",
     "Código Nacional de Seguridad y Convivencia Ciudadana", {"art-0005": "whole"},
     {"### CAPÍTULO II. BASES DE LA CONVIVENCIA Y SEGURIDAD CIUDADANA. ARTÍCULO 5o. DEFINICIÓN.":
      "### CAPÍTULO II. BASES DE LA CONVIVENCIA Y SEGURIDAD CIUDADANA."}),
    ("97-batch6", "batch6", "verify_batch6", "parse_batch6", "doc_units", "estatuto-organico-del-sistema-financiero",
     "estatuto_organico_sistema_financiero", "Estatuto Orgánico del Sistema Financiero",
     {"art-0112": "tail", "art-0183": "tail", "art-0193": "tail", "art-0218": "tail", "art-0270": "tail"}, {}),
    ("99a-batch9", "batch9", "verify_batch9", "parse_batch9", "doc_units", "reglamento-del-congreso", "ley_0005_1992",
     "Reglamento del Congreso (Ley 5 de 1992)", {"art-0309": "whole"},
     {"### ARTICUL0 309. COMPOSICIÓN Y PERIODO.": "### SECCIÓN I. COMISIÓN DE CUENTAS."}),
    ("99c-batch11", "batch11", "verify_batch11", "parse_batch11", "doc_units_hj", "sistema-general-de-participaciones",
     "ley_0715_2001", "Sistema General de Participaciones (Ley 715 de 2001)", {"art-0084a": "tail"}, {}),
]


def _lines(text: str) -> list[str]:
    return text.split("\n")[1:-1]


def headjoin_fixes(folder: str) -> list[str]:
    import re
    done = []
    for part, d, vmod, dmod, du, slug, page, title, keys, tits in HEADJOIN:
        path = os.path.join(folder, part + ".json")
        data = json.load(open(path, encoding="utf-8"))
        act = next(a for a in data["acts"] if a["slug"] == slug)
        sys.path.insert(0, os.path.join(C, d))
        D = importlib.import_module(dmod)
        E = getattr(D, "E", D)
        import headjoin
        units = {}
        for u in getattr(D, du)(page)[1:]:
            if hasattr(E, "label_num"):
                n = E.label_num(u["label"] or "")
            else:  # codes/parse_codes.py reads the number the same way (build_act)
                m = re.match(r"ART[IÍ]CULO\s+(\d+[A-Z]?)", u["label"] or "")
                n = m.group(1) if m else None
            uk = E.unit_key(n) if n else None
            if uk and uk[0] in keys and uk[0] not in units:
                units[uk[0]] = (u, uk[1])
        if sorted(units) != sorted(keys):
            sys.exit(f"{part} {page}: repaired units {sorted(units)}, expected {sorted(keys)}")
        today = importlib.import_module(vmod).V.today(page) if vmod else None
        changed = False
        tail_starts = []
        for key, how in keys.items():
            u, label = units[key]
            states = [(v, f) for v in act["versions"] for f in ("units", "changes") if key in (v.get(f) or {})]
            if how == "whole":
                if today is not None:
                    new = today[key]
                else:  # codes/verify_today.py's reading (epigraphs in angle brackets are the publisher's)
                    new = [t for t in (E.tidy(E.to_text(it[1], keep_struck=False)) for it in u["items"]
                                       if it[0] == "p" and "antsig" not in it[1]) if re.search(r"\w", t)]
                if not new:
                    sys.exit(f"{part} {key}: no text on the page")
                text = "# " + label + "\n" + "".join(l + "\n" for l in new)
                if states:
                    if any(v[f][key] is None or v[f][key]["text"] != text for v, f in states):
                        sys.exit(f"{part} {key}: the part already holds other text for it")
                    continue
                first = act["versions"][0]
                first["units"] = dict(sorted({**first["units"], key: {"label": label, "kind": "art", "text": text}}.items()))
                changed = True
            else:
                tl = headjoin.tail_lines(E, u)
                if not tl:
                    sys.exit(f"{part} {key}: empty tail")
                tail_starts += [l[:50] for l in tl]
                last = next((v[f][key] for v, f in reversed(states)), None)
                if last is None:
                    sys.exit(f"{part} {key}: not in the last version")
                old = _lines(last["text"])
                if old[-len(tl):] == tl:
                    continue  # done already
                if today is not None and today[key] != old + tl:
                    sys.exit(f"{part} {key}: the part's last text and the tail are not today's text on the page")
                for v, f in states:
                    x = v[f][key]
                    if x is not None and x["text"] == last["text"]:
                        v[f][key] = dict(x, text=last["text"] + "".join(l + "\n" for l in tl))
                        changed = True
        for v in act["versions"]:
            for field in ("units", "changes"):
                t = ((v.get(field) or {}).get("titulos") or {}).get("text")
                if not t:
                    continue
                out = []
                for l in t.split("\n")[:-1]:
                    rep = next((r for p, r in tits.items() if l.startswith(p)), False)
                    if rep is False and any(l.startswith("### " + s) for s in tail_starts):
                        rep = None
                    if rep is False:
                        out.append(l)
                    elif rep is not None:
                        out.append(rep)
                nt = "".join(l + "\n" for l in out)
                if nt != t:
                    v[field]["titulos"] = dict(v[field]["titulos"], text=nt)
                    changed = True
        if changed:
            for dec in headjoin.decision(title, headjoin.DONE.get(page)):
                if dec not in data["decisions"]:
                    data["decisions"].append(dec)
            open(path + ".tmp", "w", encoding="utf-8", newline="\n").write(
                json.dumps(data, ensure_ascii=False, separators=(",", ":")) + chr(10))
            os.replace(path + ".tmp", path)
            done.append(f"{part} {slug} " + ",".join(keys))
    return done


if __name__ == "__main__":
    main(sys.argv[1:])
