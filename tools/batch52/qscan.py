"""Quoted-article candidates: an article whose last paragraph ends 'quedará así:' followed by numbered units out of
sequence. Usage: qscan.py <page>..."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse_batch52 as B
for pg in sys.argv[1:]:
    own = None
    for u in B._units_qa(pg):
        n = u["name"] or ""
        if own and re.fullmatch(r"\d+", n) and int(n) != int(own) + 1:
            print(pg, own, "->", n, u["label"][:50]); continue
        own = None
        if re.fullmatch(r"\d+", n):
            ps = [B.E.tidy(B.E.plain(it[1])) for it in u["items"] if it[0] == "p" and B.E.tidy(B.E.plain(it[1]))]
            own = n if ps and B.QUOTES.search(ps[-1]) else None
