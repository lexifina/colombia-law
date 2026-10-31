"""Triage of the audited fallback units (fallback/.tmp/audit.json): heading-only, punctuation/accent-only, typo-level,
or substantive; for substantive ones, the later acts or rulings the unit's notes name after the last event."""
import difflib, json, os, re, sys, unicodedata
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit as A

NUMW = re.compile(r"\d|\b(uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieci\w+|"
                  r"veinte|veinti\w+|treinta|cuarenta|cincuenta|sesenta|setenta|ochenta|noventa|cien|ciento|doscientos|"
                  r"trescientos|cuatrocientos|quinientos|seiscientos|setecientos|ochocientos|novecientos|mil|millones?)\b")


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def strong(lines):
    return re.sub(r"[^a-z0-9]", "", deacc(" ".join(lines)))


def word_ops(k, t):
    kw, tw = " ".join(k).split(" "), " ".join(t).split(" ")
    return [(" ".join(kw[a:b]), " ".join(tw[c:d])) for op, a, b, c, d in
            difflib.SequenceMatcher(None, kw, tw, autojunk=False).get_opcodes() if op != "equal"]


def kind(x):
    k, t = A.body(x["known_last"]), A.body(x["today"])
    if k == t:
        return "heading"
    if not k or not t:
        return "K0" if not k else "T0"
    if strong(k) == strong(t):
        return "punct"
    ops = word_ops(k, t)
    if len(ops) <= 3 and not any(NUMW.search(a + " " + b) for a, b in ops) and \
            all(difflib.SequenceMatcher(None, a, b).ratio() >= 0.6 for a, b in ops if a and b) and \
            sum(len(a) + len(b) for a, b in ops) <= 40:
        return "typo"
    return "subst"


def later(x):
    ev = {l for _, l in x["events"]}
    last = x["events"][-1][0]
    return sorted({(k, d) for k, d in x.get("named", []) if k not in ev and d and d > last}, key=lambda e: e[1])


if __name__ == "__main__":
    rows = json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))
    out, cnt = [], Counter()
    for r in rows:
        if "records" not in r:
            out.append(dict(tag=r["tag"], unit=r["unit"], kind="no-record")); cnt["no-record"] += 1; continue
        ks = [kind(x) for x in r["records"]]
        order = ["subst", "K0", "T0", "typo", "punct", "heading"]
        worst = min(ks, key=order.index)
        x = r["records"][ks.index(worst)]
        lt = later(x)
        out.append(dict(tag=r["tag"], unit=r["unit"], kind=worst, later=lt, nrec=len(ks)))
        cnt[(worst, min(len(lt), 2))] += 1
    for c, n in sorted(cnt.items(), key=str):
        print(c, n)
    json.dump(out, open(os.path.join(A.TMP, "triage.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "-v" in sys.argv:
        for o in out:
            if o["kind"] in ("typo", "punct"):
                print(o["tag"], o["unit"], o["kind"])
