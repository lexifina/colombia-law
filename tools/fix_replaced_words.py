"""Repair words the source shows replaced in place ('<S>old</S> <new*>') in corpus.d/90-batch4.json, without re-parsing
the part (its parser, as restored, no longer reproduces it byte for byte).

The engine read the struck words as struck and the bracketed new words as an editor's marker, so both were lost (Ley 100
de 1993, art. 41: '... ante una deficiencia, discapacidad que hayan generado secuelas ...'). The page reads '<*Texto
corregido en los términos de la Sentencia C-458-15> ... discapacidad <S>y minusvalía</S> <e invalidez*>': the old words
'y minusvalía' until Sentencia C-458 de 2015 (22 July 2015), which ordered them read as 'e invalidez', and the new words
from that day, credited to the ruling. phase2/subst.py does the same when later batches are parsed.

For each entry this script checks the page in the cache, puts the old words into every version's text before the day and
the new words from it (adding the change to the version on that day), and drops the ruling's note 'It did not change the
words'. Idempotent.

Usage:  python -X utf8 fix_replaced_words.py [corpus.d folder]
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import engine as E  # noqa: E402

FIXES = [  # (part, act slug, page, unit key, words as the part has them, old words, new words, ruling, its day, page marks)
    ("90-batch4.json", "sistema-de-seguridad-social-integral", "ley_0100_1993", "art-0041",
     "deficiencia, discapacidad que hayan generado secuelas", "deficiencia, discapacidad y minusvalía que hayan generado "
     "secuelas", "deficiencia, discapacidad e invalidez que hayan generado secuelas", "c-458-15", "2015-07-22",
     ["discapacidad <S>y minusval&iacute;a</S> &lt;e invalidez*&gt;",
      "&lt;*Texto corregido en los t&eacute;rminos de la Sentencia <A href=\"c-458_2015.html#C-458-15\" >C-458-15</A>&gt;"]),
]


def check_page(page: str, marks: list[str]) -> None:
    html = "".join(E.read(E.BASE + pg + ".html") or "" for pg in E.pages(page))
    for m in marks:
        if html.count(m) != 1:
            raise SystemExit(f"{page}: {m!r} found {html.count(m)} times")


def fix(path, slug, key, have, old, new, law, day) -> bool:
    with open(path, encoding="utf-8") as f:
        part = json.load(f)
    act = next(a for a in part["acts"] if a["slug"] == slug)
    changed = False
    for v in act["versions"]:
        src = v.get("units") if "units" in v else v.get("changes")
        u = (src or {}).get(key)
        if u and have in u["text"]:
            src[key] = dict(u, text=u["text"].replace(have, old if v["from"] < day else new))
            changed = True
    on_day = [v for v in act["versions"] if v["from"] == day]
    if len(on_day) != 1:
        raise SystemExit(f"{slug}: {len(on_day)} versions on {day}")
    v = on_day[0]
    if "units" in v:
        raise SystemExit(f"{slug} {day}: a full version")
    if (v.get("changes") or {}).get(key) is None:
        # the text in force just before that day, with the new words
        cur = None
        for w in act["versions"]:
            if w["from"] >= day:
                break
            src = w.get("units") if "units" in w else w.get("changes")
            if src and key in src:
                cur = src[key]
        if cur is None or old not in cur["text"]:
            raise SystemExit(f"{slug} {key}: old words not in the text before {day}")
        v.setdefault("changes", {})[key] = dict(cur, text=cur["text"].replace(old, new))
        changed = True
    if law not in (v["credits"].get(key) or []):
        v["credits"][key] = sorted(set(v["credits"].get(key) or []) | {law})
        changed = True
    if part["laws"][law].get("note"):
        part["laws"][law]["note"] = None
        changed = True
    d = (f"Sistema de Seguridad Social Integral (Ley 100 de 1993): words the source shows replaced in place (art. 41: "
         f"'<S>y minusvalía</S> <e invalidez*>', with the marker 'Texto corregido en los términos de la Sentencia "
         f"C-458-15') read as the old words before {day} and as the new words from it, credited to Sentencia C-458 de 2015.")
    if d not in part["decisions"]:
        part["decisions"].append(d)
        changed = True
    if changed:
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    return changed


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d")
    for part, slug, page, key, have, old, new, law, day, marks in FIXES:
        check_page(page, marks)
        print(part, key, "changed" if fix(os.path.join(out, part), slug, key, have, old, new, law, day) else "unchanged")
