"""Take the engine's false 'did not change the words' note off conditional rulings that also changed words, in place.

The engine gives every ruling it reads as conditional (exequibilidad condicionada) the law note phase2/condnotes.COND
('... It did not change the words.'), which the builder prints on every commit of the law. About 75 rulings, each held
by one part, also struck or replaced words in some version credited to them, so the note was false there. For every law
whose note is COND in some part and whose credited units change words in any part holding it (a version credited to
the ruling alone; an act's first day with rulings folded into it does not count), the note goes from every part's entry
(all entries then agree, null) and each part that had it gets one decision line naming the provisions where the ruling
changed no words (phase2/condnotes.sentence). Text, credits and versions are untouched. Generic: no list of laws; laws
whose note is true keep it. phase2/parse_phase2.write_part applies the same rule to every part it writes, so a re-parse
gives the same result. Idempotent (a part whose notes are already off is left alone).

RE-RUN ORDER: last, after every other fix_* script (fix_shared_notes.py and fix_law_entries.py included), after any
re-parse of an older part.

Usage: python -X utf8 fix_conditional_notes.py [corpus.d folder]
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import condnotes as CN  # noqa: E402


def dump(part):
    return json.dumps(part, ensure_ascii=False, separators=(",", ":")) + "\n"


def main(folder):
    # corpus.json (the Constitution) sits next to corpus.d; a trial folder holds its own copy among the parts.
    top = [] if os.path.exists(os.path.join(folder, "corpus.json")) else [os.path.join(os.path.dirname(folder), "corpus.json")]
    paths = top + sorted(glob.glob(os.path.join(folder, "*.json")))
    parts, holders = {}, {}
    for p in paths:
        raw = open(p, encoding="utf-8").read()
        d = json.loads(raw)
        parts[p] = (raw, d)
        for k in d.get("laws", {}):
            holders.setdefault(k, []).append(p)
    noted = sorted({k for p, (_, d) in parts.items() for k, law in d.get("laws", {}).items() if law.get("note") == CN.COND})
    for p in sorted({p for k in noted for p in holders[k]}):
        if dump(parts[p][1]) != parts[p][0]:
            raise SystemExit(f"{p}: does not re-serialise byte for byte")
    evs = {k: {p: CN.events(parts[p][1]["acts"], k) for p in holders[k]} for k in noted}
    touched = set()
    for k in noted:
        if not CN.changes_words([e for es in evs[k].values() for e in es]):
            continue  # the note is true
        for p in holders[k]:
            d = parts[p][1]
            if d["laws"][k].get("note") != CN.COND:
                continue
            others = {k: [e for q, es in evs[k].items() if q != p for e in es]}
            lines = CN.resolve({k: d["laws"][k]}, d["acts"], others)
            for line in lines:
                if line in d["decisions"]:
                    raise SystemExit(f"{p} {k}: decision already there")
                d["decisions"].append(line)
            touched.add(p)
            same = [(e[0], e[1], e[2]) for e in evs[k][p] if not e[4]]
            print(f"{os.path.basename(p)} {k}: note removed; unchanged units {same}")
    for p in sorted(touched):
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(dump(parts[p][1]))
        os.replace(tmp, p)
    print("parts written:", len(touched), " ".join(os.path.basename(p) for p in sorted(touched)) or "(none: applied)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d"))
