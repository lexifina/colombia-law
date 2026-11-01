"""Deferred strikes the parts date wrongly, fixed in place in the published parts (2026-11-01, seventeenth session).

Two kinds of entry:

- 'move' (coordinator decision 99c-batch11, 2026-11-01): a ruling that kept the struck text in force for a term counted
  from its NOTIFICATION, where no source gives the notification day and the earliest possible end of the term has
  passed. The text leaves on the ruling's day plus the term (the earliest day the term can end), credited to the
  ruling, with a decision line saying the exact day depends on the unknown notification day. The part had taken the
  text out on the ruling's own day: that version's removal moves to the end of the term.
- 'strike': a deferred strike whose end day the page states, which the part never applied (the words stand to today):
  the given lines leave on that day, credited to the ruling (a new version if none is on that day).
- 'move_text' (coordinator decision, 2026-11-01, twenty-seventh session): a deferred strike whose end day the page
  states, which the part applied on the ruling's own day (the earlier text back): that change moves, unchanged, to the
  stated day, so the struck text stays in force until then (settled rule: a deferred strike leaves on the deferral's
  stated day).

Each entry is checked against its page (the deferral must be quoted there). Idempotent: an entry whose result is
already in the part is skipped. RE-RUN ORDER: after fallback/apply.py and fix_dated_struck.py / fix_multi_struck.py,
before fix_box_text.py, after any re-parse of the parts below (99c-batch11, 98-batch7, 99h-batch16).

Usage: python -X utf8 fix_deferrals.py [corpus.d folder]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_c253_deferral as C253  # noqa: E402  (page_text)

MARK = "Deferral ends (2026-11-01)"
CE18 = "Otorga el plazo de un (1) año contado a partir de la notificación de la presente sentencia"
ENTRIES = [
    {"kind": "move", "part": "99c-batch11.json", "slug": "estatuto-organico-de-bogota", "page": "decreto_1421_1993",
     "ruling": "ce-2018-06-06", "day": "2018-06-06", "end": "2019-06-06",
     "units": ["art-0087", "art-0088", "art-0090", "art-0092", "art-0094"],
     "quote": [CE18, "Una vez cumplido el plazo indicado"],
     "decision": "Estatuto Orgánico de Bogotá (Decreto 1421 de 1993), arts. 87, 88, 90, 92 and 94 (fondos de desarrollo "
                 "local): the Consejo de Estado (Sala Plena, Sentencia of 6 June 2018, Expediente No. "
                 "11001-03-15-000-2008-01255-00) declared them NULO and gave the Concejo de Bogotá one (1) year from the "
                 "ruling's notification to regulate the matter; the articles stop producing effects when that year ends, "
                 "or when the Concejo's regulation is adopted if that comes first. No source gives the notification day "
                 "(the page names no regulation by the Concejo either), and the year has certainly passed, so the "
                 "articles leave on 6 June 2019, the ruling's day plus one year, credited to the ruling: the exact day "
                 "depends on the unknown notification day, and 6 June 2019 is the earliest it can be. They had been "
                 "shown out of force from the ruling's own day."},
    {"kind": "strike", "part": "98-batch7.json", "slug": "codigo-de-recursos-naturales", "page": "decreto_2811_1974",
     "ruling": "c-148-22", "day": "2023-07-19", "unit": "art-0273",
     "quote": ["4o. <Numeral INEXEQUIBLE, con efectos difeidos hasta el 19 de julio de 2023> Deportiva",
               "Numeral declarado INEXEQUIBLE, con efectos difeidos por el término de un (1) año contado a partir de la "
               "notificación, por la Corte Constitucional mediante Sentencia C-148-22 de 27 de abril de 2022",
               "Notificada mediante Edicto de 19 de julio de 2022"],
     "old": "4o. Deportiva, o sea la que se efectúa como recreación o ejercicio, sin otra finalidad que su realización misma.",
     "new": "4o.",
     "law": {"label": "Sentencia C-148 de 2022", "title": "Corte Constitucional, Sentencia C-148 de 2022", "kind": "court",
             "enacted": "2022-04-27", "published": None,
             "url": "http://www.secretariasenado.gov.co/senado/basedoc/c-148_2022.html", "temporary_until": None,
             "restores": None, "note": None},
     "decision": "Código de Recursos Naturales Renovables (Decreto Ley 2811 de 1974), art. 273 numeral 4o. (sport "
                 "fishing): Sentencia C-148 de 2022 (27 April 2022) declared it INEXEQUIBLE with its effects deferred one "
                 "(1) year from the ruling's notification, which the page gives (edicto of 19 July 2022; its marker reads "
                 "'efectos diferidos hasta el 19 de julio de 2023'): the numeral's words stand until 19 July 2023 and "
                 "leave that day, credited to the ruling; its number stays, as for art. 252 literal c). The words had "
                 "been kept to today."},
    # (eighteenth session, coordinator decision on Decreto 1333 art. 233 literal a)) a temporary exequibility whose term
    # runs from an unknown notification day: the words leave on the earliest day the term can end.
    {"kind": "strike", "part": "99h-batch16.json", "slug": "codigo-de-regimen-municipal", "page": "decreto_1333_1986",
     "ruling": "c-221-97", "day": "2002-04-29", "unit": "art-0233",
     "quote": ["Literal declarado TEMPORALMENTE EXEQUIBLE por la Corte Constitucional mediante Sentencia C-221-97",
               "y en forma temporal por un plazo de cinco años contados a partir de la notificación de la presente "
               "sentencia, el literal a) del artículo 233 del Decreto 1333 de 1986",
               "Expedida durante este término la correspondiente norma legal, el literal a) del artículo 233 del Decreto "
               "1333 de 1986 será INEXEQUIBLE",
               "Una vez expirado el término señalado de cinco años, y en caso de que (SIC) Congreso no haya establecido el "
               "correspondiente régimen de regalías para la extracción de la arena, el cascajo y la piedra del lecho de los "
               "ríos, el literal a) del Decreto 1333 de 1986 será INEXEQUIBLE",
               "mediante el artículo 16 de la Ley 756 de 2002, publicada en el Diario Oficial No. 44.878, de 25 de julio de "
               "2002, se incluye dentro de las regalías, los materiales de construcción",
               "mediante la Ley 685 de 2001, publicada en el Diario Oficial No. 44.545, de 8 de septiembre de 2001, se "
               "expide expide el Código de Minas y se dictan otras disposiciones. Ver artículos 11 y 227"],
     "old": "a. Impuesto de extracción de arena, cascajo y piedra del lecho de los cauces de ríos y arroyos, dentro de los "
            "términos municipales, sin perjudicar el laboreo y el aprovechamiento legítimos de las minas y de las aguas.",
     "new": "a.",
     "law": {"label": "Sentencia C-221 de 1997", "title": "Corte Constitucional, Sentencia C-221 de 1997", "kind": "court",
             "enacted": "1997-04-29", "published": None,
             "url": "http://www.secretariasenado.gov.co/senado/basedoc/c-221_1997.html", "temporary_until": None,
             "restores": None, "note": None},
     "decision": "Código de Régimen Municipal (Decreto 1333 de 1986), art. 233 literal a) (the municipal tax on taking "
                 "sand, gravel and stone from river beds): Sentencia C-221 de 1997 (29 April 1997; the page's box dates it "
                 "1999, a slip the ruling's own page corrects) held it EXEQUIBLE only for five (5) years from the ruling's "
                 "notification, urged Congress to set within that term the royalties for the non-renewable resources not "
                 "yet subject to one, and ordered that the literal becomes INEXEQUIBLE once such a law is issued within "
                 "the term, or else when the term ends. The editor's notes point to Ley 685 de 2001 (Código de Minas, in "
                 "force 8 September 2001, within the term), whose art. 11 makes river sand, gravel and stones 'materiales "
                 "de construcción' and whose art. 227 makes every exploitation of State-owned non-renewable resources "
                 "owe a royalty without setting its rate, and to art. 16 of Ley 756 de 2002 (25 July 2002), which first "
                 "set a royalty for 'Materiales de construcción' (1%) but falls within the term only if the ruling was "
                 "notified on or after 25 July 1997. Neither law certainly set those royalties within the term, so the "
                 "literal leaves on 29 April 2002, the ruling's day plus five years, the earliest day the term can end "
                 "(which has passed), credited to the ruling: the exact day depends on the notification day, which no "
                 "source gives. Its letter stays, as for art. 252 c). The page still prints the literal with no marker; "
                 "it had been kept to today."},
    # (twenty-seventh session, coordinator decision 1) Decreto 111 de 1996 art. 29: C-052-15 deferred its strike of Ley
    # 1687 de 2013 art. 81 to 31 December 2015, as hf107.fix_12 has it for Ley 179 art. 12 (the same words).
    {"kind": "move_text", "part": "99c-batch11.json", "slug": "estatuto-organico-del-presupuesto",
     "page": "decreto_0111_1996", "ruling": "c-052-15", "day": "2015-02-12", "end": "2015-12-31",
     "units": ["art-0029"],
     "quote": ["Artículo 81 de la Ley 1687 de 2013 declarado INEXEQUIBLE, con los efectos diferidos hasta el 31 de "
               "diciembre de 2015, por la Corte Constitucional mediante Sentencia C-052-15 de 12 de febrero de 2015"],
     "decision": "Estatuto Orgánico del Presupuesto (Decreto 111 de 1996), art. 29 (contribuciones parafiscales): "
                 "Sentencia C-052 de 2015 (12 February 2015) declared Ley 1687 de 2013 art. 81, which had rewritten it "
                 "from 11 December 2013, INEXEQUIBLE with its effects deferred until 31 December 2015 (the page's box: "
                 "'con los efectos diferidos hasta el 31 de diciembre de 2015'): Ley 1687's text stays in force until "
                 "then and the earlier text (Ley 225 de 1995's) is back from 31 December 2015, credited to the ruling, "
                 "as for Ley 179 de 1994 art. 12. It had been back from the ruling's own day."},
]


def states(act, key):
    out, cur = [], None
    for v in act["versions"]:
        if "units" in v:
            cur = (v["units"].get(key) or {}).get("text")
        if key in (v.get("changes") or {}):
            u = v["changes"][key]
            cur = u and u.get("text")
        out.append(cur)
    return out


def version_on(vs, day):
    k = next((k for k, v in enumerate(vs) if v["from"] >= day), len(vs))
    if k < len(vs) and vs[k]["from"] == day:
        return vs[k]
    prev = vs[k - 1]
    v = {"from": day, "credits": {}, "changes": {}}
    for f in ("source_url", "sha256"):
        if f in prev:
            v[f] = prev[f]
    vs.insert(k, v)
    return v


def touches(v, key):
    return key in (v.get("changes") or {}) or key in v["credits"] or "units" in v


def do_move(part, act, e):
    vs = act["versions"]
    done = []
    for key in e["units"]:
        before = dict(zip([v["from"] for v in vs], states(act, key)))
        at_end = [v for v in vs if v["from"] == e["end"] and (v.get("changes") or {}).get(key, 0) is None
                  and v["credits"].get(key) == [e["ruling"]]]
        if at_end:
            if any(v["from"] == e["day"] and key in v["credits"] for v in vs):
                raise SystemExit(f"{key}: removal on both days")
            continue
        old = [v for v in vs if v["from"] == e["day"] and v["credits"].get(key) == [e["ruling"]]]
        if len(old) != 1 or "units" in old[0] or (old[0].get("changes") or {}).get(key, 0) is not None:
            raise SystemExit(f"{key}: no removal on {e['day']} credited to {e['ruling']} alone")
        if any(e["day"] < v["from"] <= e["end"] and touches(v, key) for v in vs):
            raise SystemExit(f"{key}: another change before {e['end']}")
        v = old[0]
        del v["changes"][key]
        del v["credits"][key]
        if not v["credits"] and not v.get("changes"):
            vs.remove(v)
        w = version_on(vs, e["end"])
        w.setdefault("changes", {})[key] = None
        w["credits"][key] = [e["ruling"]]
        # check: unchanged before the ruling's day; the text in force just before it stays until the end day; absent after
        prior = before[max(d for d in before if d < e["day"])]
        for v, s in zip(vs, states(act, key)):
            d = v["from"]
            want = before[d] if d < e["day"] else (prior if d < e["end"] else None)
            if s != want or (e["day"] <= d < e["end"] and s is None):
                raise SystemExit(f"{key}: states do not come out as wanted on {d}")
        done.append(key)
    # the fallback audit's decision lines named the ruling's day
    old_tail = "out of force from " + e["day"] + " ("
    for i, d in enumerate(part["decisions"]):
        if e["ruling"] in d or ("de 6 de junio de 2018" in d and "Decreto 1421" in d):
            if old_tail in d and "shown out of force from the ruling's day" in d:
                part["decisions"][i] = (d.replace(old_tail, "out of force from " + e["end"] + " (")
                                        .replace("; shown out of force from the ruling's day",
                                                 "; shown out of force from the earliest day that year can end, "
                                                 "the notification day being unknown (" + MARK + ")"))
    return done


def do_move_text(part, act, e):
    """The change credited to the ruling alone on its own day moves, with the same text, to the deferral's end day."""
    vs = act["versions"]
    done = []
    for key in e["units"]:
        before = dict(zip([v["from"] for v in vs], states(act, key)))
        at_end = [v for v in vs if v["from"] == e["end"] and key in (v.get("changes") or {})
                  and v["credits"].get(key) == [e["ruling"]]]
        if at_end:
            if any(v["from"] == e["day"] and key in v["credits"] for v in vs):
                raise SystemExit(f"{key}: the ruling's change on both days")
            continue
        old = [v for v in vs if v["from"] == e["day"] and v["credits"].get(key) == [e["ruling"]]]
        if (len(old) != 1 or "units" in old[0] or key not in (old[0].get("changes") or {})
                or old[0]["changes"][key] is None):
            raise SystemExit(f"{key}: no text change on {e['day']} credited to {e['ruling']} alone")
        if any(e["day"] < v["from"] <= e["end"] and touches(v, key) for v in vs):
            raise SystemExit(f"{key}: another change before {e['end']}")
        v = old[0]
        unit = v["changes"].pop(key)
        del v["credits"][key]
        if not v["credits"] and not v.get("changes"):
            vs.remove(v)
        w = version_on(vs, e["end"])
        w.setdefault("changes", {})[key] = unit
        w["credits"][key] = [e["ruling"]]
        # check: unchanged before the ruling's day; the text in force just before it stays until the end day; from
        # the end day the text the ruling's day had
        prior = before[max(d for d in before if d < e["day"])]
        for v, s in zip(vs, states(act, key)):
            d = v["from"]
            want = before[d] if d < e["day"] else (prior if d < e["end"] else before.get(d, unit["text"]))
            if s != want or s is None:
                raise SystemExit(f"{key}: states do not come out as wanted on {d}")
        done.append(key)
    return done


def do_strike(part, act, e):
    vs = act["versions"]
    key = e["unit"]
    st = states(act, key)
    if e["ruling"] in (next((v for v in vs if v["from"] == e["day"]), {"credits": {}})["credits"].get(key) or []):
        if any(s is not None and e["old"] in s for v, s in zip(vs, st) if v["from"] >= e["day"]):
            raise SystemExit(f"{key}: credited but the words are still there")
        return []
    if any(v["from"] > e["day"] and touches(v, key) for v in vs):
        raise SystemExit(f"{key}: a change after {e['day']}: not handled")
    k = max(i for i, v in enumerate(vs) if v["from"] < e["day"])
    t = st[k]
    if t is None or t.count(e["old"]) != 1:
        raise SystemExit(f"{key}: words not once in the text on {vs[k]['from']}")
    unit = None
    for v in vs[:k + 1]:
        if "units" in v and key in v["units"]:
            unit = v["units"][key]
        if key in (v.get("changes") or {}):
            unit = v["changes"][key]
    w = version_on(vs, e["day"])
    w.setdefault("changes", {})[key] = dict(unit, text=t.replace(e["old"], e["new"]))
    w["credits"][key] = [e["ruling"]]
    if e["ruling"] not in part["laws"]:
        part["laws"][e["ruling"]] = dict(e["law"])
    after = states(act, key)
    if after[:vs.index(w)] != st[:vs.index(w)] or e["old"] in after[-1]:
        raise SystemExit(f"{key}: states do not come out as wanted")
    return [key]


def main(argv):
    out = argv[0] if argv else os.path.join(HERE, "corpus.d")
    # One pass per part: the part's lines go (or move) to the end, in ENTRIES order, after the lines the earlier fixes
    # in the re-run order re-append or move (fix_multi_struck moves its line to the end on every run); the part is
    # written only if that or an entry changes it, so a re-run of the whole order is a no-op, also with two entries in
    # one part.
    for name in dict.fromkeys(e["part"] for e in ENTRIES):
        path = os.path.join(out, name)
        part = json.load(open(path, encoding="utf-8"))
        lines, changed = [], False
        for e in [e for e in ENTRIES if e["part"] == name]:
            t = C253.page_text(e["page"])
            for q in e["quote"]:
                if q not in t:
                    raise SystemExit(f"{e['page']}: not quoted: {q[:80]}")
            act = next(a for a in part["acts"] if a["slug"] == e["slug"])
            done = {"move": do_move, "move_text": do_move_text, "strike": do_strike}[e["kind"]](part, act, e)
            line = f"{MARK}: {e['decision']}"
            lines.append(line)
            if done or part["decisions"].count(line) != 1:
                changed = True
            print(name, e["slug"], ("applied: " + ", ".join(done)) if done else
                  ("already applied" if part["decisions"].count(line) == 1 else "applied: (decision line only)"))
        decisions = [d for d in part["decisions"] if d not in lines] + lines
        if not changed and decisions == part["decisions"]:
            continue
        part["decisions"] = decisions
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
        print(name, "written")


if __name__ == "__main__":
    main(sys.argv[1:])
