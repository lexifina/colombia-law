"""Words the source puts in angle brackets as the text a ruling ordered, under a marker that itself contains '<>':
'<Texto entre <> corregido en los términos de la Sentencia C-458-15> ... a <personas en situación de discapacidad física,
sensorial y psíquica>, ...' (Ley 115 de 1994, arts. 1 and 46). The engine's marker reading stops at the inner '<>', so it
left the marker's tail ('corregido en los términos de la Sentencia C-458-15>') in the text and dropped the bracketed
words as an editor's note. install(E, pages) rewrites those pages' HTML as E.read returns it: the marker goes, and the
bracketed words after it in the same article (up to the next anchor) are kept as text.
"""
from __future__ import annotations

import re

MARK = re.compile(r"&lt;Textos? entre\s*&lt;&gt;(?:&#160;|\s)*corregidos? en los t&eacute;rminos de la Sentencia\s*"
                  r"(?:<A [^>]*>)?C-458-15(?:</A>)?&gt;(?:&#160;|\s)*", re.I)
WORDS = "&lt;personas en situaci&oacute;n de discapacidad f&iacute;sica, sensorial y ps&iacute;quica&gt;"
PLAIN = "personas en situaci&oacute;n de discapacidad f&iacute;sica, sensorial y ps&iacute;quica"
SEEN: dict[str, int] = {}


def rewrite(page: str, html: str) -> str:
    out, pos = [], 0
    for m in MARK.finditer(html):
        out.append(html[pos:m.start()])
        nxt = re.search(r'<a\s+(?:class="bookmarkaj"\s+)?name=', html[m.end():], re.I)
        end = m.end() + (nxt.start() if nxt else len(html) - m.end())
        seg = html[m.end():end]
        SEEN[page] = SEEN.get(page, 0) + seg.count(WORDS)
        out.append(seg.replace(WORDS, PLAIN))
        pos = end
    out.append(html[pos:])
    return "".join(out)


def install(E, pages: set[str]) -> None:
    read = E.read
    if getattr(read, "_nested_pages", None) is not None:
        read._nested_pages |= set(pages)
        return
    ref = set(pages)

    def read_any(url: str):
        t = read(url)
        if t is None or not url.endswith(".html"):
            return t
        base = re.sub(r"_pr\d{3}$", "", url.rsplit("/", 1)[-1][:-5])
        return rewrite(base, t) if base in ref else t

    read_any._nested_pages = ref
    E.read = read_any
