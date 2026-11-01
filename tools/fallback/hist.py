"""Print one unit's dated history from a corpus part.  Usage: python -X utf8 fallback/hist.py <part.json> <act slug> <unit key> [--full]"""
import json
import sys


def history(part: dict, slug: str, key: str) -> list[tuple[str, list, str | None]]:
    """[(from, credits, text or None)] for each version where the unit's text changes or it is credited."""
    a = next(x for x in part["acts"] if x["slug"] == slug)
    out, cur = [], None
    for v in a["versions"]:
        if "units" in v:
            val = (v["units"].get(key) or {}).get("text")
        elif key in v.get("changes", {}):
            val = (v["changes"][key] or {}).get("text")
        else:
            val = cur
        if val != cur or key in v.get("credits", {}):
            out.append((v["from"], v.get("credits", {}).get(key), val))
        cur = val
    return out


if __name__ == "__main__":
    part = json.load(open(sys.argv[1], encoding="utf-8"))
    for d, cr, t in history(part, sys.argv[2], sys.argv[3]):
        print(d, cr)
        print("   ", (t or "NONE") if "--full" in sys.argv else (t or "NONE")[:400].replace("\n", " | "))
