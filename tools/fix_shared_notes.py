"""Take part-specific 'no words changed' notes off shared law entries, in place.

A law's `note` is printed on every commit of that law, and the builder keeps the first part's entry for a law key that
several parts share. Some notes are true for one part only:
- Decreto 538 de 2020: 50-codes' note ('... limited literal g) of art. 4 ... It changed no words.') is true for Ley 1581
  art. 4 but the decree changes words in six other parts;
- conditional rulings: the engine's note ('upheld this text on a condition of interpretation ... It did not change the
  words.') is on rulings that also strike or replace words in this or another part.

For each law in LAWS: the note goes from every part's entry (all entries then agree, null), and each part that had the
note gets one decision line naming the units credited to the law where it changed no words (the fact now lives only
there). Commits then print the builder's standard line (words changed, or not) for each day. Text, credits and versions
are untouched. Each law's note must still read as expected, and some credited unit must change words somewhere (else
the note is true and stays). Idempotent (decision mark). RE-RUN after any re-parse of a part named in PARTS_HINT.

Usage: python -X utf8 fix_shared_notes.py [corpus.d folder]
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "Shared law notes (2026-11-01)"
COND = ("A Constitutional Court ruling that upheld this text on a condition of interpretation (exequibilidad "
        "condicionada). It did not change the words.")
D538 = ("Decreto Legislativo 538 de 2020, art. 8, limited literal g) of art. 4 (security of data) to the technical, "
        "human and administrative security measures of health providers while the COVID-19 health emergency lasted. "
        "It changed no words.")
LAWS = {"dec-538-2020": D538, **{k: COND for k in (
    "c-039-25", "c-112-19", "c-370-06", "c-384-00", "c-428-19", "c-447-25", "c-448-97", "c-514-19", "c-518-16",
    "c-525-23", "c-527-17", "c-570-19", "c-750-15", "c-616-02",
    # (batch 93) C-555-94: conditional in 99-batch8, struck Ley 60 de 1993 art. 6 parágrafo 1o. in 99zzzzzzzz-093-batch93
    "c-555-94")}}
PARTS_HINT = ("50-codes 80-batch3 90-batch4 95-batch5 97-batch6 99c-batch11 99e-batch13 99g-batch15 99k-batch19 "
              "99l-batch20 99zk-batch45 99zq-batch51 99zr-batch52 99zy-batch59 99zze-batch65 99zzi-batch69 "
              "99zzl-batch72 99-batch8 99zzzzzzzz-093-batch93 99zzzzzzzz-098-batch98")


def dump(part):
    return json.dumps(part, ensure_ascii=False, separators=(",", ":")) + "\n"


def events(part, key):
    """(act short, day, unit key, unit label, words changed) for every unit credited to `key`."""
    out = []
    for a in part["acts"]:
        st = {}
        for v in a["versions"]:
            prev = st
            if "units" in v:
                st = dict(v["units"])
            elif "changes" in v:
                st = dict(st)
                for k, u in v["changes"].items():
                    if u is None:
                        st.pop(k, None)
                    else:
                        st[k] = u
            for k, c in v["credits"].items():
                if key in c:
                    old, new = prev.get(k), st.get(k)
                    label = (new or old or {}).get("label", k)
                    out.append((a["short"], v["from"], k, label, (old or {}).get("text") != (new or {}).get("text")))
    return out


def sentence(label, key, evs):
    if key == "dec-538-2020":
        return (f"{MARK}: {label}, art. 8, limited literal g) of Ley 1581 de 2012 art. 4 (security of data) to the "
                f"technical, human and administrative security measures of health providers while the COVID-19 health "
                f"emergency lasted, from 2020-04-12; it changed no words of LPDP Art. 4. The decree changes words of "
                f"other acts, so its law entry carries no note.")
    byday = {}
    for short, day, _, ulabel, _ in evs:
        byday.setdefault((day, short), []).append(ulabel)
    what = "; ".join(f"{short} {', '.join(ls)} on {day}" for (day, short), ls in sorted(byday.items()))
    return (f"{MARK}: {label} upheld these provisions on a condition of interpretation (exequibilidad condicionada) "
            f"and changed no words of them: {what}. The ruling changes words elsewhere, so its law entry carries no note.")


def main(folder):
    paths = sorted(glob.glob(os.path.join(folder, "*.json")))
    parts = {}
    for p in paths:
        raw = open(p, encoding="utf-8").read()
        d = json.loads(raw)
        if any(k in d.get("laws", {}) for k in LAWS):
            if dump(d) != raw:
                raise SystemExit(f"{p}: does not re-serialise byte for byte")
            parts[p] = d
    touched = set()
    for key, note in LAWS.items():
        holders = [p for p, d in parts.items() if key in d.get("laws", {})]
        noted = [p for p in holders if parts[p]["laws"][key].get("note")]
        if not noted:
            continue  # applied already (or re-parse gave none)
        for p in noted:
            if parts[p]["laws"][key]["note"] != note:
                raise SystemExit(f"{p} {key}: unexpected note {parts[p]['laws'][key]['note']!r}")
        evs = {p: events(parts[p], key) for p in holders}
        if not any(e[4] for es in evs.values() for e in es):
            raise SystemExit(f"{key}: no part changes words, the note is true")
        for p in noted:
            d = parts[p]
            same = [e for e in evs[p] if not e[4]]
            if same:
                line = sentence(d["laws"][key]["label"], key, same)
                if line in d["decisions"]:
                    raise SystemExit(f"{p} {key}: decision already there")
                d["decisions"].append(line)
            d["laws"][key]["note"] = None
            touched.add(p)
            print(f"{os.path.basename(p)} {key}: note removed; unchanged units {[(e[0], e[1], e[2]) for e in same]}")
    for p in sorted(touched):
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(dump(parts[p]))
        os.replace(tmp, p)
    print("parts written:", len(touched), " ".join(os.path.basename(p) for p in sorted(touched)) or "(none: applied)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d"))
