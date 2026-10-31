"""Move article words that were read as a heading back into their article, in parts that cannot be re-parsed here
(corpus.d/95-batch5.json), without re-parsing them.

The basedoc sometimes starts a block of an article with an anchor that has no heading of its own but is named like a
section heading ('TITULO I'); the engine took the block for a heading, so its words went into titulos.md and the article
lost them. phase2/stray.py repairs this when later batches are parsed. Here:
- Código Nacional de Tránsito (Ley 769 de 2002), art. 52, whose last paragraph 'PARÁGRAFO. Los vehículos automotores de
  placas extranjeras ...' stood in titulos.md (95-batch5);
- Ley de Víctimas y Restitución de Tierras (Ley 1448 de 2011), art. 91A (added by Ley 2294 de 2023), whose last two
  paragraphs ('Las medidas contempladas en el presente artículo ...' and 'PARÁGRAFO. Cuando los jueces de la República
  ...') stand under two anchors named 'TÍTULO I' (99-batch8: its driver installs phase2/stray.py only after its own
  main() has run, so the part was built without it; verify_batch8 imports the driver and so reads them).

For each entry the script checks the page in the cache, then in every version it takes the lines out of titulos.md
(where they stand there) and adds them at the end of the article's text (where that version has the article and the
line is not there yet), and recomputes the changes of each version from the repaired texts. Idempotent.

Usage:  python -X utf8 fix_stray_headings.py [corpus.d folder]
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import engine as E  # noqa: E402

FIXES = [  # (part, act slug, page, anchor name on the page, unit key, article number, the lines, decision)
    ("95-batch5.json", "codigo-nacional-de-transito", "ley_0769_2002", "TITULO I", "art-0052", "52",
     ["PARÁGRAFO. Los vehículos automotores de placas extranjeras, que ingresen temporalmente y hasta por tres (3) meses "
      "al país, no requerirán la revisión técnico-mecánica y de emisiones contaminantes."],
     "Código Nacional de Tránsito (Ley 769 de 2002): art. 52's last paragraph ('PARÁGRAFO. Los vehículos automotores de "
     "placas extranjeras ...') stands on the page under an anchor with no heading of its own named 'TITULO I'; it is "
     "a paragraph of the article, not a heading (fix_stray_headings.py)."),
    ("99-batch8.json", "ley-de-victimas-y-restitucion-de-tierras", "ley_1448_2011", "TÍTULO I", "art-0091a", "91A",
     ["Las medidas contempladas en el presente artículo se aplicarán por una sola vez y por núcleo familiar para quienes "
      "tengan relación con el predio objeto de restitución, la cual deberá ser anterior a la macro focalización de la "
      "zona intervenida, reconocidos como tal en las providencias judiciales de restitución de tierras.",
      "PARÁGRAFO. Cuando los jueces de la República ordenen a la Unidad Administrativa Especial de Gestión de Restitución "
      "de Tierras realizar caracterización socioeconómica, esta se realizará por una sola vez a los habitantes del "
      "predio, conforme la metodología que defina dicha Unidad."],
     "Ley de Víctimas y Restitución de Tierras (Ley 1448 de 2011): art. 91A's last two paragraphs ('Las medidas "
     "contempladas en el presente artículo ...' and 'PARÁGRAFO. Cuando los jueces de la República ...') stand on the "
     "page under two anchors with no heading of their own named 'TÍTULO I'; they are paragraphs of the article, not "
     "headings (fix_stray_headings.py)."),
]


def check_page(page: str, anchor: str, num: str, lines: list[str]) -> None:
    """The lines stand, in order, in the unlabelled blocks named `anchor` right after the article."""
    units = E.doc_units(page)
    for i, u in enumerate(units):
        if E.label_num(u["label"] or "") != num:
            continue
        got = []
        for v in units[i + 1:]:
            if v["name"] != anchor or (v["label"] or "").strip():
                break
            got += [t for t in (E.tidy(E.to_text(it[1])) for it in v["items"] if it[0] == "p") if t]
        if got == lines:
            return
    raise SystemExit(f"{page}: blocks '{anchor}' with the lines not found after art. {num}")


def full_states(versions):
    cur, out = {}, []
    for v in versions:
        if "units" in v:
            cur = dict(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append(cur)
    return out


def fix(path, slug, key, lines, d) -> bool:
    with open(path, encoding="utf-8") as f:
        part = json.load(f)
    act = next(a for a in part["acts"] if a["slug"] == slug)
    vs = act["versions"]
    states = full_states(vs)
    new_states, changed = [], False
    for st in states:
        st = dict(st)
        for line in lines:
            t = st.get("titulos")
            head = f"### {line}\n"
            if t and head in t["text"]:
                st["titulos"] = dict(t, text=t["text"].replace(head, ""))
                changed = True
            u = st.get(key)
            if u and line not in u["text"]:
                st[key] = dict(u, text=u["text"] + line + "\n")
                changed = True
        new_states.append(st)
    if not changed:
        return False
    prev = None
    for v, st in zip(vs, new_states):
        if "units" in v:
            v["units"] = st
        elif "changes" in v or prev is not None:
            ch = {k: u for k, u in st.items() if prev.get(k) != u}
            ch.update({k: None for k in prev if k not in st})
            if "changes" in v or ch:
                v["changes"] = ch
            for k in ("titulos", key):
                if k in v["credits"] and k not in ch and not any(k == x for x in ch):
                    # a credit for a change that no longer exists (the line moved): the unit is unchanged that day
                    if k == "titulos":
                        v["credits"].pop(k)
        prev = st
    if d not in part["decisions"]:
        part["decisions"].append(d)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    return True


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d")
    for part, slug, page, anchor, key, num, lines, d in FIXES:
        check_page(page, anchor, num, lines)
        print(part, key, "changed" if fix(os.path.join(out, part), slug, key, lines, d) else "unchanged")
