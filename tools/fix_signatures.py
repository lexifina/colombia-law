"""Cut the signature blocks that the parsers left at the end of the last article of some acts ('El Presidente del
Honorable Senado de la República, ...', 'La Presidenta del honorable Senado ...', 'Publíquese y cúmplase. Dado en ...',
'República de Colombia - Gobierno Nacional', ...). The general rule (phase2/parse_phase2.py SIGN_OFF) matched only some
openings ('El Presidente del Senado', lower-case 'honorable', capitals 'PUBLÍQUESE Y ...'), so blocks opening otherwise
stayed in the text. Signatures, the place and date of issue and the signers' names are not words of the act.

For every unit text in every part: from the first line that opens a signature block, the rest of the text is cut, with
the signer's name or names standing on the lines just before it (a line in capitals, or a 'Dada en ...' line). Every
cut is printed for review; a cut that would leave a unit empty, or remove a line that does not look like part of a
signature block, stops the run. Idempotent (a text with no block is left as it is).

Usage:  python -X utf8 fix_signatures.py [--dry-run] [corpus.d folder]
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OPEN = re.compile(
    r"^(?:(?:El|La) (?:[Pp]residen(?:te|ta)|[Ss]ecretari[oa](?: [Gg]eneral)?)(?: \(E\.?\))? (?:del|de la) (?:(?:[Hh]onorable|H\.) )?"
    r"(?:Senado|Cámara)|Secretario General del (?:[Hh]onorable )?Senado|República de Colombia\s*-\s*Gobierno Nacional|"
    r"(?:Publíquese|PUBLÍQUESE|Comuníquese|COMUNÍQUESE)(?:,)? y (?:cúmplase|ejecútese|CÚMPLASE|EJECÚTESE)|Cordialmente,$)")
# Lines a signature block is made of (checked on everything cut).
BLOCK = re.compile(
    r"^(?:(?:El|La) [A-ZÁÉÍÓÚa-záéíóúñ ]+(?:,|\.)?$|[^a-záéíóúñ]+$|[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?: [A-ZÁÉÍÓÚÑ][a-záéíóúñ]+| de| del| la){1,6}[.,]?$|"
    r"Dad[oa] en .*|.{0,60}(?:mil novecientos|dos mil|\((?:19|20)\d\d\)).{0,40}|.{0,80}(?i:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre).{0,60}|(?:Santafé de )?Bogotá,? D\.? ?[CE]\..*|.*\b(?:Presiden|Secretari|Ministr|Director|Viceministr|Jefe)\w*\b.*|República de Colombia.*|"
    r"(?:Publíquese|Comuníquese|PUBLÍQUESE|COMUNÍQUESE).*|Cordialmente,|de mil novecientos.*|del mes de .*|"
    r"(?:General|Brigadier|Almirante|Mayor) .*|\(E\.?\)|.{0,3})$")


def cut(text: str) -> tuple[str, list[str]]:
    lines = text.split("\n")
    body = lines[1:-1] if text.endswith("\n") else lines[1:]
    i = next((k for k, l in enumerate(body) if OPEN.match(l)), None)
    if i is None:
        return text, []
    while i > 0 and (re.fullmatch(r"[^a-záéíóúñ]+", body[i - 1]) and re.search(r"[A-ZÁÉÍÓÚÑ]{3}", body[i - 1])
                     or re.match(r"Dad[oa] en ", body[i - 1])):
        i -= 1
    gone = body[i:]
    if not body[:i]:
        raise SystemExit(f"cut would empty the unit: {gone[:3]}")
    bad = [l for l in gone if not BLOCK.match(l)]
    if bad:
        raise SystemExit(f"not a signature line: {bad[:3]} in {gone[:6]}")
    return "\n".join([lines[0]] + body[:i]) + "\n", gone


def main(argv):
    dry = "--dry-run" in argv
    folder = next((a for a in argv if not a.startswith("--")), os.path.join(HERE, "corpus.d"))
    files = [os.path.join(os.path.dirname(folder.rstrip("/\\")), "corpus.json")] + sorted(glob.glob(os.path.join(folder, "*.json")))
    for f in files:
        if not os.path.exists(f):
            continue
        part = json.load(open(f, encoding="utf-8"))
        touched = {}
        for a in part.get("acts", []):
            for v in a["versions"]:
                for field in ("units", "changes"):
                    for k, u in list((v.get(field) or {}).items()):
                        if not u:
                            continue
                        t, gone = cut(u["text"])
                        if gone:
                            v[field][k] = dict(u, text=t)
                            touched.setdefault((a["slug"], k), gone)
        if not touched:
            continue
        for (s, k), gone in touched.items():
            print(f"{os.path.basename(f)} {s} {k}: cut {len(gone)} lines: {' / '.join(gone[:3])[:150]}")
        if not dry:
            line = ("Signature blocks at the end of the last article ('El Presidente del Honorable Senado de la "
                    "República, ...', 'La Presidenta del honorable Senado ...', 'Publíquese y cúmplase. Dado en ...') are "
                    "not part of the text and are cut (fix_signatures.py): "
                    + "; ".join(f"{s} {k}" for s, k in sorted(touched)) + ".")
            part.setdefault("decisions", [])
            part["decisions"] = [d for d in part["decisions"] if not d.startswith("Signature blocks at the end of the last article")]
            part["decisions"].append(line)
            tmp = f + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(part, fh, ensure_ascii=False, separators=(",", ":"))
                fh.write("\n")
            os.replace(tmp, f)


if __name__ == "__main__":
    main(sys.argv[1:])
