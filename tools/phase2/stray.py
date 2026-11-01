"""Stray anchors: blocks the basedoc starts with an anchor that has no heading of its own (its name a section heading's,
'TITULO I', 'CAPÍTULO I', or a number) although they hold words of an article.

- A block whose first paragraph starts 'ARTÍCULO N.' is that article (its heading moved into the anchor).
- A block of running text (it has lower-case words) right after an article (or after such a block) is the rest of that
  article: its paragraphs and note boxes are joined to it.
A block of capitals only is left alone: it is the name of the heading above.

Without this, the engine took such blocks for headings (their text went into titulos.md) or for a duplicate of an
article named by the anchor, so the article lost those paragraphs, or a whole article was missing. The checks read
today's text through the same blocks, so they could not see it.

repair(name, units) returns the units repaired and records what it did in DONE[name].
"""
from __future__ import annotations

import re

DONE: dict[str, list[str]] = {}
ART_HEAD = re.compile(r"\s*(?:<span class=\"b_aj\">)?\s*(ART(?:Í|&Iacute;|I)CULO\s+(\d+[A-Z]?)(?:o|º)?\.\s*"
                      r"((?:(?!</span>)[^<a-zñ])*?\.)?)\s*(?:</span>)?\s*", re.S)


def repair(name: str, units: list[dict], E) -> list[dict]:
    out, done = [], []
    for u in units:
        if not out or (u["label"] or "").strip() or u["name"] == "_head":
            out.append(u)
            continue
        ps = [k for k, it in enumerate(u["items"]) if it[0] == "p"]
        text = " ".join(E.plain(u["items"][k][1]) for k in ps).strip()
        if not text or all("antsig" in u["items"][k][1] for k in ps if E.plain(u["items"][k][1]).strip()):
            out.append(u)
            continue
        first = next((k for k in ps if E.plain(u["items"][k][1]).strip()), None)
        h = u["items"][first][1] if first is not None else ""
        bold = re.match(r"\s*<B>(.*?)</B>\s*", h, re.S | re.I)
        hb = re.match(r"\s*(ART[ÍI]CULO\s+(\d+[A-Z]?)(?:o|º)?\.)", E.plain(bold.group(1))) if bold else None
        m = None if hb else ART_HEAD.match(h)
        prev = out[-1]
        if hb or m:
            anchor = u["name"]
            num = hb.group(2) if hb else m.group(2)
            label = E.tidy(E.plain(bold.group(1))) if hb else E.tidy(E.plain(m.group(1)))
            rest = h[bold.end():] if hb else h[m.end():]
            u = dict(u, name=num, label=label)
            u["items"] = list(u["items"])
            u["items"][first] = ("p", rest) + tuple(u["items"][first][2:])
            done.append(f"art. {num} (its heading in the text, under an anchor named '{anchor}')")
            out.append(u)
            continue
        article_like = (re.match(r"(PAR[ÁA]GRAFO|INCISO|NUMERAL|LITERAL|\d+[\.\)]|[a-z][\.\)]\s)", text)
                        or (len(text.split()) >= 12 and re.search(r"[a-záéíóúñ]{3}", text)))
        if article_like and re.match(r"ART[ÍI]CULO", prev["label"] or ""):
            prev["items"] = list(prev["items"]) + list(u["items"])
            done.append(f"art. {E.label_num(prev['label']) or prev['name']} ({len(ps)} paragraphs under an anchor named "
                        f"'{u['name']}')")
            continue
        out.append(u)
    if done:
        DONE[name] = done
    return out


# Unnumbered 'ARTÍCULO NUEVO.' articles (added by a later act without a number). The drivers' NEW_ARTS table maps a
# heading to a file by the heading alone, for every page, so a second act's 'ARTÍCULO NUEVO.' would take the first act's
# file (Ley 270 de 1996's art-0209-nuevo). On the pages given, each such article is the file art-NNNN-nuevo-K after the
# numbered article NNNN above it.
NEW_DONE: dict[str, list[str]] = {}
NEW_HEAD = re.compile(r"\s*ART[ÍI]CULO\s+NUEVO\s*\.\s*(.*)$")


def new_articles(name: str, units: list[dict], E, new_keys: dict) -> list[dict]:
    prev_num, k, done = None, 0, []
    for u in units[1:]:
        m = NEW_HEAD.match(u["label"] or "")
        num = E.label_num(u["label"] or "") if not m else None
        if num and num.isdigit():
            prev_num, k = int(num), 0
            continue
        if m and prev_num is not None:
            k += 1
            code = f"{name}:NUEVO:{prev_num}:{k}"
            new_keys[code] = (f"art-{prev_num:04d}-nuevo-{k}", f"Art. nuevo {k} (después del art. {prev_num})")
            u["name"] = code
            # A heading no article-number reading (nor the NEW_ARTS table) matches; the engine strips 'ARTÍCULO NUEVO'.
            u["label"] = "ARTÍCULO NUEVO ." + (" " + m.group(1) if m.group(1) else "")
            done.append(f"art-{prev_num:04d}-nuevo-{k}")
    if done:
        NEW_DONE[name] = done
    return units
