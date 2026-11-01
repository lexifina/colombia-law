"""Hand-set histories for batch 95 (Ley 141 de 1994), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import difflib
import re

import hand_fixes as H  # noqa: F401
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fix_c253_deferral as C253  # noqa: E402  (page_text)

L141, S141 = "ley_0141_1994", "regalias-1994"
T141 = "Fondo Nacional de Regalías y regalías (Ley 141 de 1994)"
L619, C737, C737_RULING_DAY, C737_END = "ley-619-2000", "c-737-01", "2001-07-11", "2002-06-20"
L619_DAY = "2000-10-20"
C737_QUOTE = ("los efectos de la anterior declaración de INEXEQUIBILIDAD quedan diferidos hasta el 20 de junio de 2002, a fin "
              "de que el Congreso, dentro de la libertad de configuración que le es propia, expida el régimen que subrogue "
              "la Ley 619 de 2000")
# Units Ley 619 de 2000 changed (the page's notes: 'modificado/adicionado/derogado por el artículo N de la Ley 619 de 2000').
UNITS_619 = (1, 5, 9, 10, 13, 14, 15, 16, 17, 29, 35, 41, 43, 49, 50, 62)
INSIDE_OK = {"ley-685-2001", "c-427-02"}
OWN_FIX = (1, 5, 9, 16, 29)  # Ley 619 units whose whole history is set by their own fix below  # changes inside the deferral (Código de Minas; Sentencia C-427 de 2002)


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


def _need(c, what):
    H.B23._need(c, what)


def _u(num):
    return H.B23._unit(L141, str(num))


def _nonav(lines):
    """The page's navigation links ('Anterior', 'Siguiente') after an article are not its words."""
    return [l for l in lines if not re.fullmatch(r"(?:Anterior|Siguiente)(?:\s*\|\s*(?:Anterior|Siguiente))?", l.strip())]


def _key(num):
    return f"art-{int(num):04d}"


def _units_on(act, days):
    """A version on one of `days` that carries no units gets a copy of the units before it (hf89 rule)."""
    full = None
    for v in act["versions"]:
        if "units" in v:
            full = v["units"]
        elif v["from"] in days:
            v["units"] = dict(full)
            full = v["units"]


def _apply(act, key, tl):
    _units_on(act, {d for d, _, _ in tl[1:]})
    H._set(act, key, H._label(act, key), tl)
    H.B23._forget(L141, key)


def merge3(base, ours, theirs):
    """Lines: base -> theirs edits laid over ours (base -> ours: the text Ley 619 de 2000 replaced coming back). An edit
    of theirs touching lines ours also changes is dropped: ours wins there (the later change was to Ley 619's words)."""
    if ours is None or base is None:
        return ours

    def edits(other):
        return [(i1, i2, other[j1:j2]) for tag, i1, i2, j1, j2 in
                difflib.SequenceMatcher(None, base, other, autojunk=False).get_opcodes() if tag != "equal"]
    eo, et = edits(ours), edits(theirs)

    def clash(a1, a2):
        return any((c1 <= a1 <= c2) if a1 == a2 else ((a1 <= c1 <= a2) if c1 == c2 else (a1 < c2 and c1 < a2))
                   for c1, c2, _ in eo)
    out, pos = [], 0
    for i1, i2, repl in sorted(eo + [e for e in et if not clash(e[0], e[1])], key=lambda e: (e[0], e[1])):
        out += base[pos:i1] + repl
        pos = i2
    return out + base[pos:]


def fix_c737(act):
    """Ley 619 de 2000 (in force 20 October 2000), which rewrote or added to arts. 1, 5, 9, 10, 13 to 17, 29, 35, 41,
    43, 49, 50 and 62, was declared INEXEQUIBLE as a whole by Sentencia C-737 de 2001 (11 July 2001), whose order, quoted
    under the articles, defers the effect: 'Conforme a lo expuesto en el fundamento 55 de esta sentencia, los efectos de la
    anterior declaración de INEXEQUIBILIDAD quedan diferidos hasta el 20 de junio de 2002'. As for Sentencia C-253 de
    2010's deferral, Ley 619's words stand until 20 June 2002, and that day the words it had replaced come back, credited to
    the ruling, until Ley 756 de 2002 (25 July 2002). Changes made inside the deferral stay where they touched words
    Ley 619 had not written: on art. 10, Sentencia C-427 de 2002 (29 May 2002) struck 'irresponsable o' in numeral 4,
    which Ley 619 had not touched (the ruling's box stands under numeral 4): that strike stays, while numeral 1, which Ley
    619 had rewritten, takes its earlier words back. Art. 13, which
    Ley 619 repealed (tacitly, Sentencia C-672 de 2002), is back from 20 June 2002 and out again from 25 July 2002: the
    Court held it 'hubiera recobrado vigencia si no hubiera sido expedida la Ley 756 de 2002'. Art. 62's text before Ley
    619, which only added its parágrafo, is the article without that parágrafo (from the act's first day as well). The
    engine had brought the earlier words back on the ruling's day for nine articles and never for the other seven.
    (Arts. 1, 5, 9, 16 and 29 follow the same rule within the full histories set for them below.)"""
    E = H.E
    _need(C737_QUOTE in H._jv(_u(1)), "Ley 141: C-737-01 deferral quote")
    _need("hubiera recobrado vigencia si no hubiera sido expedida la Ley 756 de 2002" in H._jv(_u(13)), "art. 13 C-672-02")
    _need("Parágrafo adicionado por el artículo 16 de la Ley 619 de 2000" in H._nv(_u(62)), "art. 62 NV")
    c737 = E.register(C737) if C737 not in E.LAWS else C737
    for n in UNITS_619:
        key = _key(n)
        if n in OWN_FIX:
            continue  # fix_9, fix_1, fix_5, fix_16, fix_29
        h = H._hist(act, key)
        days = [d for d, _, _ in h]
        _need(L619_DAY in days and h[days.index(L619_DAY)][2] == [L619], f"Ley 141 art. {n}: no Ley 619 change {H._shape(h)}")
        i619 = days.index(L619_DAY)
        pre = h[i619 - 1][1]
        t619 = h[i619][1]
        if n == 62:
            _need(pre == [H.PH] and t619 and t619[-1].startswith("PARÁGRAFO"), f"art. 62 {H._shape(h)}")
            pre = t619[:-1]
        inside = [x for x in h[i619 + 1:] if x[0] < C737_END]
        after = [x for x in h[i619 + 1:] if x[0] >= C737_END]
        for d, b, c in inside:
            _need(c == [C737] and d == C737_RULING_DAY or (c and set(c) <= INSIDE_OK), f"art. {n}: inside {d} {c}")
        kept = [x for x in inside if x[2] != [C737]]
        last = kept[-1][1] if kept else t619
        revived = pre if last == t619 else merge3(t619, pre, last)
        tl = [(None, h[0][1] if n != 62 else pre, None)] + [(d, b, c[0]) for d, b, c in h[1:i619]]
        tl += [(L619_DAY, t619, L619)] + [(d, b, c[0]) for d, b, c in kept] + [(C737_END, revived, c737)]
        if n == 13:
            _need(not after, f"art. 13 after {H._shape(h)}")
            after = [("2002-07-25", None, ["ley-756-2002"])]
        _need(all(c and len(c) == 1 for _, _, c in after), f"art. {n}: after {H._shape(h)}")
        tl += [(d, b, c[0]) for d, b, c in after]
        _apply(act, key, tl)
    H._done(T141, fix_c737)


def fix_9(act):
    """art. 9 (the Comisión Nacional de Regalías' members): the source prints today's text and, in its boxes, the
    original numeral 4o. (changed by Ley 344 de 1996, art. 7) and the original parágrafo 2o. and Ley 619 de 2000's
    (Ley 756 de 2002 rewrote it again). Decreto 1178 de 1999 (29 June 1999) repealed the article and Sentencia C-722 de
    1999 (29 September 1999) struck that decree, bringing it back. So: the article as enacted; numeral 4o. from 31 December
    1996; out from 29 June 1999; back from 29 September 1999; parágrafo 2o. as Ley 619 wrote it from 20 October 2000 until
    Sentencia C-737 de 2001's deferral ended on 20 June 2002 (the original parágrafo back), then Ley 756 de 2002's from 25
    July 2002. The engine had a placeholder from 1994 and Decreto 1178's day as the first text."""
    u = _u(9)
    nv, box = H._nv(u), " ".join(H.E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior")
    _need("Artículo derogado por el artículo 22 del Decreto 1178 de 1999" in nv and "Parágrafo 2o. modificado por el artículo 7 "
          "de la Ley 619 de 2000" in nv and "El Decreto 1178 de 1999 fue declarado INEXEQUIBLE por la Corte Constitucional, "
          "mediante Sentencia C-722-99 del 29 de Septiembre de 1999" in H._jv(u), "art. 9 notes")
    o4 = "4. El Ministro de Desarrollo o en su defecto el Viceministro."
    m = re.search(r"Texto modificado por la Ley 619 de 2000:\s*(PARÁGRAFO 2o\. .*?)\s*Texto original de la Ley 141 de 1994:\s*"
                  r"(PARÁGRAFO 2o\. .*?país\.)", box)
    _need(o4 in box and m, "art. 9 boxes")
    p619, p94 = (re.sub(r"\s+", " ", x).strip() for x in m.groups())
    h = H._hist(act, "art-0009")
    _need([(d, c) for d, _, c in h] == [("1994-06-30", None), ("1999-06-29", ["dec-1178-1999"]), (L619_DAY, [L619]),
                                        ("2002-07-25", ["ley-756-2002"])], f"art. 9 {H._shape(h)}")
    now = h[-1][1]
    i4 = [i for i, l in enumerate(now) if l.startswith("4. ")]
    ip = [i for i, l in enumerate(now) if l.startswith("PARÁGRAFO 2o.")]
    _need(len(i4) == len(ip) == 1 and h[2][1][ip[0]] == p619, f"art. 9 lines {i4} {ip}")
    t96 = now[:ip[0]] + [p94] + now[ip[0] + 1:]
    t94 = t96[:i4[0]] + [o4] + t96[i4[0] + 1:]
    t619 = now[:ip[0]] + [p619] + now[ip[0] + 1:]
    _need(t619 == h[2][1], "art. 9: Ley 619 text")
    _apply(act, "art-0009", [(None, t94, None), ("1996-12-31", t96, "ley-344-1996"), ("1999-06-29", None, "dec-1178-1999"),
                             ("1999-09-29", t96, "c-722-99"), (L619_DAY, t619, L619), (C737_END, t96, C737),
                             ("2002-07-25", now, "ley-756-2002")])
    H._done(T141, fix_9)


def kept_paragraph(num):
    """Arts. 21 and 22: the page's lines for today, '<Artículo derogado, salvo el parágrafo ...>' and '...' left out."""
    u = _u(num)
    ps = [it for it in u["items"] if it[0] == "p"]
    _need(len(ps) == 3 and "Art&iacute;culo derogado, salvo el par&aacute;grafo" in ps[0][1]
          and H.E.plain(ps[1][1]).strip() == "...", f"art. {num}: page shape")
    return _nonav(H._printed(dict(u, items=[it for it in u["items"] if it[0] != "p" or it is ps[2]])))


def fix_21_22(act):
    """arts. 21 and 22 (base prices for hydrocarbon and coal royalties): repealed save their parágrafo (1o.) by art. 160
    of Decreto 4923 de 2011, in force from 1 January 2012 ('Rige a partir del 1o. de enero de 2012', the notes), and again
    by art. 160 of Ley 1530 de 2012 (17 May 2012), which changed no further words and makes no version. The original-text
    box prints art. 21's inciso, '...' where its parágrafo 1o. stands, and its parágrafo 2o., and art. 22's inciso alone:
    the article as enacted is that inciso with the parágrafo the page prints in force today (and art. 21's parágrafo 2o.);
    from 1 January 2012 only the parágrafo (under the article's heading). The engine had the enacted text without the
    kept parágrafo and only the parágrafo from Ley 1530's day."""
    for num, n_box in ((21, 2), (22, 1)):
        u, key = _u(num), _key(num)
        _need(f"derogado por el artículo 160 del Decreto 4923 de 2011, publicado en el Diario Oficial No. 48.294 de 26 de "
              f"diciembre de 2011. Rige a partir del 1o. de enero de 2012" in H._nv(u), f"art. {num} NV")
        h = H._hist(act, key)
        _need([(d, c) for d, _, c in h] == [("1994-06-30", None), ("2012-05-17", ["ley-1530-2012"])] and len(h[0][1]) == n_box,
              f"art. {num} {H._shape(h)}")
        kept = kept_paragraph(num)
        _need(len(kept) == 1 and kept[0].split(". ", 1)[1].startswith("PARÁGRAFO"), f"art. {num} kept {kept}")
        par = "PARÁGRAFO" + kept[0].split("PARÁGRAFO", 1)[1]
        t94 = [h[0][1][0], par] + h[0][1][1:]
        _apply(act, key, [(None, t94, None), ("2012-01-01", kept, "dec-4923-2011")])
    H._done(T141, fix_21_22)


FNR_UNITS = (32, 33, 34, 37, 39)
CORPES_UNITS = (40, 46, 47)


def fix_struck_lines(act):
    """The lines the page shows struck in arts. 32 to 47, which the engine had left out of every version (no ruling
    dates them): (a) the Fondo Nacional de Regalías' share in arts. 32, 33, 34 (twice), 37 and 39 - art. 18, parágrafo
    1o., of Ley 1530 de 2012 (17 May 2012), which the notes quote, adds the shares 'distribuidas al Fondo Nacional de
    Regalías ... a que hacen referencia los artículos 31 al 37 y el 39 de la Ley 141 de 1994' to the producing
    departments and municipalities: in force from the act's first day, out from 17 May 2012, credited to it (the notes add
    that Decreto 4923 de 2011 had been issued transitorily before it, without naming its provision); (b) the Corpes'
    share in art. 40 and the Fondo de Inversión Regional's in arts. 46 and 47, struck as tacitly repealed: Sentencia C-251
    de 2003, quoted under them, holds that the Corpes and their Fondo de Inversión Regional ceased to exist, art. 51 of Ley
    152 de 1994 as extended by art. 1 of Ley 290 de 1996 keeping the Corpes 'hasta el 1º de enero del año 2.000': in force
    from the act's first day, out from 1 January 2000, credited to Ley 290 de 1996."""
    E = H.E
    l290 = E.register("ley-290-1996")
    for nums, day, law, ev in ((FNR_UNITS, "2012-05-17", "ley-1530-2012", "a que hacen referencia los artículos 31 al 37 y "
                                "el 39 de la Ley 141 de 1994, se sumarán de manera proporcional"),
                               (CORPES_UNITS, "2000-01-01", l290, "prorrogado así la vigencia de estos Consejos hasta el 1º "
                                "de enero del año 2.000")):
        for num in nums:
            u, key = _u(num), _key(num)
            _need(ev in (H._nv(u) + " " + H._jv(u)), f"art. {num}: note")
            before, after = _nonav(H._printed(u, keep_struck=True)), _nonav(H._printed(u))
            h = H._hist(act, key)
            _need([(d, c) for d, _, c in h] == [("1994-06-30", None)] and h[0][1] == after and len(before) > len(after),
                  f"art. {num} {H._shape(h)}")
            _apply(act, key, [(None, before, None), (day, after, law)])
    H._done(T141, fix_struck_lines)


# ---------------------------------------------------------------- (eighteenth session) full histories

HDR = re.compile(r"^(?:PAR[AÁ]GRAFO|Par[aá]grafo)\b")


def _norm(s):
    return re.sub(r"[^\w%]+", "", s).lower()


def _blocks(lines):
    """[lines before the first parágrafo, then one list per parágrafo (its header line first)]."""
    out = [[]]
    for l in lines:
        if HDR.match(l):
            out.append([])
        out[-1].append(l)
    return out


def _flat(blocks):
    return [l for b in blocks for l in b]


def _box(u):
    return " ".join(H.E.plain(b) for b in H.B23._boxes(u, "Legislación Anterior"))


def _orig_seg(u):
    """The 'Texto original de la Ley 141 de 1994' parts of the article's earlier-text boxes (normalised)."""
    return [_norm(x.split("Texto modificado por")[0]) for x in _box(u).split("Texto original de la Ley 141 de 1994")[1:]]


def _cut_mix(block, today, orig):
    """A parágrafo block the engine took from the original-text box, with today's lines of that parágrafo still after
    it: the block up to the first line that is today's and no original text holds; every line from there must be
    today's (they are dropped)."""
    for i, l in enumerate(block):
        if l in today and not any(_norm(l) in o for o in orig):
            _need(all(x in today for x in block[i:]), f"mixed block tail {block[i][:60]}")
            return block[:i], block[i:]
    return block, []


def _struck_paras(u, after):
    """The paragraphs of the first earlier-text box holding `after`, from there to the next 'Texto ...' heading, each
    as (words with the struck spans, words without them)."""
    raw = next((x for x in H.B23._boxes(u, "Legislación Anterior") if after in x), None)
    _need(raw, f"box marker {after}")
    out = []
    for p in re.split(r"(?i)</?p\b[^>]*>", raw.split(after, 1)[1]):
        a, b = H.E.tidy(H.E.to_text(p, True)), H.E.tidy(H.E.to_text(p, False))
        if a.startswith("Texto "):
            break
        if re.search(r"\w", a):
            out.append((a, b))
    return out


def _set_credits(act, key, day, laws):
    v = next(v for v in act["versions"] if v["from"] == day)
    _need(v["credits"].get(key) == laws[:1], f"{key} {day} credit")
    v["credits"][key] = list(laws)


def E_reg(key):
    return H.E.register(key) if key not in H.E.LAWS else key


def fix_1(act):
    """art. 1 (the Fondo Nacional de Regalías): the engine had laid parágrafos 1o. and 5o. as enacted (from the
    original-text boxes) over today's lines of the same parágrafos, which Ley 756 de 2002 wrote (numerals 1 and 2 of
    parágrafo 1o. and its 'El reglamento' line; numerals 1 to 10 and literals a) to c) of parágrafo 5o.), so every
    version before 25 July 2002 held both: those lines of today's text now arrive with Ley 756 de 2002. Parágrafo 2o.:
    Ley 344 de 1996, art. 3, rewrote it in the words the box gives, in force from 21 March 1997, the day Decreto 799 de
    1997 published the correction that headed that article 'El parágrafo 2o. del artículo 1o. de la Ley 141 de 1994
    quedará así' (the note dates the change by that Diario Oficial No. 43.008; 99zzzzzzzz-094-batch94 dates the corrected
    words of Ley 344 the same way), credited to both; Sentencia C-497 de 1998 (15 September 1998) struck that article
    ('sólo tendrá efectos hacia el futuro, a partir de la notificación del presente fallo': the ruling's day, as in
    batch 94), so the original parágrafo is back that day; Ley 508 de 1999 (30 July 1999) rewrote it and Sentencia C-557
    de 2000 (16 May 2000) struck that law as a whole, so the original is back again that day; then Ley 685 de 2001
    (8 September 2001) and Ley 756 de 2002. Parágrafo 4o.: Ley 619 de 2000's words until Sentencia C-737 de 2001's
    deferral ended on 20 June 2002, the original back that day, then Ley 756 de 2002 and Ley 858 de 2003. The engine
    had Ley 344's words from 31 December 1996 and Ley 508's to 8 September 2001."""
    E = H.E
    u = _u(1)
    jv = H._jv(u)
    _need("El artículo 3o. de la Ley 344 de 1996 fue declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia "
          "C-497-98 de 15 de septiembre de 1998" in jv and "sólo tendrá efectos hacia el futuro, a partir de la "
          "notificación del presente fallo" in jv and "La Ley 508 de 1999 fue declarada INEXEQUIBLE por la Corte "
          "Constitucional, mediante sentencia C-557-00 de 16 de mayo de 2000" in jv, "art. 1 JV")
    _need("Parágrafo 2o. modificado por el artículo 3o. de la Ley 344 de 1996, publicada en el Diario Oficial No. 43.008 "
          "de 21 de marzo de 1997" in H._nv(u), "art. 1 NV Ley 344")
    h = H._hist(act, "art-0001")
    want = [None, ["ley-344-1996"], ["ley-508-1999"], [L619], ["ley-685-2001"], ["ley-756-2002"], ["ley-858-2003"]]
    _need([c for _, _, c in h] == want, f"art. 1 {H._shape(h)}")
    today = set(h[-1][1])
    orig = _orig_seg(u)
    bl = [_blocks(b) for _, b, _ in h]
    _need(all(len(b) == 6 for b in bl[:6]), "art. 1 blocks")
    for b in bl[:5]:  # parágrafos 1o. and 5o., as the engine had them before Ley 756
        for j in (1, 5):
            b[j], tail = _cut_mix(b[j], today, orig)
            _need(tail and all(l in bl[5][j] for l in tail), f"art. 1 par {j} tail")
    o = bl[0]
    for i, j in ((1, 2), (2, 2), (3, 4), (4, 2)):  # each engine version changes one parágrafo of the one before
        _need(all(bl[i][k] == bl[i - 1][k] for k in range(6) if k != j) and bl[i][j] != bl[i - 1][j], f"art. 1 v{i}")
    p2 = {"o": o[2], "344": bl[1][2], "508": bl[2][2], "685": bl[4][2]}
    p4 = {"o": o[4], "619": bl[3][4]}

    def t(b2, b4):
        return _flat([o[0], o[1], b2, o[3], b4, o[5]])
    c497 = E.add_court("C-497-98", "1998-09-15", "c-497_1998.html")
    c557 = E.add_court("C-557-00", "2000-05-16", "c-557_2000.html")
    E_reg("dec-799-1997")
    _apply(act, "art-0001", [(None, t(p2["o"], p4["o"]), None),
                             ("1997-03-21", t(p2["344"], p4["o"]), "ley-344-1996"),
                             ("1998-09-15", t(p2["o"], p4["o"]), c497),
                             ("1999-07-30", t(p2["508"], p4["o"]), "ley-508-1999"),
                             ("2000-05-16", t(p2["o"], p4["o"]), c557),
                             (L619_DAY, t(p2["o"], p4["619"]), L619),
                             ("2001-09-08", t(p2["685"], p4["619"]), "ley-685-2001"),
                             (C737_END, t(p2["685"], p4["o"]), E_reg(C737)),
                             ("2002-07-25", h[5][1], "ley-756-2002"),
                             ("2003-12-29", h[6][1], "ley-858-2003")])
    _set_credits(act, "art-0001", "1997-03-21", ["ley-344-1996", "dec-799-1997"])
    H._done(T141, fix_1)


def fix_5(act):
    """art. 5 (the share of the Fondo's yearly takings for the listed territorial projects, its parágrafo): the engine
    had a placeholder from 1994 and, from 31 December 1996 to 25 July 2002, today's numerals 1 to 18 laid beside the
    boxes' earlier texts. Set from the 'Legislación Anterior' box and the amending acts as the page prints them: the
    criteria and the parágrafo as enacted (12.625%, numerals 1 to 16 and its two closing incisos) from the act's first
    day; Ley 344 de 1996, art. 43 (31 December 1996), adds numeral 17 (Ciénaga de Zapatoza, 0.5%) and so raises the share
    to 13.125%; Ley 619 de 2000, art. 8 (20 October 2000), rewrites inciso 1o. (13%) and gives numeral 17 to Sincelejo
    (0.375%; the editor's note: with the total of 13% the earlier numeral 17 cannot also stand); Ley 685 de 2001, art. 359
    (8 September 2001), rewrites inciso 1o. again (13.5%, its words as Ley 685's own page prints them, the box cutting
    them short) and adds numeral 18 (Ciénaga de Zapatoza, with El Banco); when Sentencia C-737 de 2001's deferral of Ley
    619's strike ended on 20 June 2002, Ley 619's numeral 17 went and Ley 344's numeral 17 came back, while Ley 685's
    inciso 1o. and numeral 18, written after Ley 619, stayed (the shares then add up to more than the inciso's 13.5%: so
    the acts read); Ley 756 de 2002, art. 6 (25 July 2002), rewrote the parágrafo as the page prints it today."""
    u = _u(5)
    box = _box(u)
    _need(C737_QUOTE in H._jv(u), "art. 5 JV")
    nv = H._nv(u)
    for q in ("Parágrafo modificado por el artículo 6 de la Ley 756 de 2002", "Numeral 18. adicionado por el artículo 359 "
              "de la Ley 685 de 2001", "Inciso 1o. modificado por el artículo 359 de la Ley 685 de 2001", "Numeral 17. "
              "adicionado por el artículo 8 de la Ley 619 de 2000", "si se suman los dos porcentajes que se encuentran bajo "
              "numeral 17, se sobrepasa al total", "Numeral 17. adicionado por el artículo 43 de la Ley 344 de 1996"):
        _need(q in nv, f"art. 5 NV {q[:40]}")
    segs = re.split(r"Texto (?:modificado por la (Ley \d+ de \d{4})|original de la Ley 141 de 1994):", box)
    seg = dict(zip([x or "orig" for x in segs[1::2]], segs[2::2]))
    _need(list(seg) == ["Ley 685 de 2001", "Ley 619 de 2000", "Ley 344 de 1996", "orig"], f"art. 5 box {list(seg)}")
    inc = {}
    for k in ("Ley 619 de 2000", "Ley 344 de 1996"):
        m = re.search(r"<INCISO 1o\.>\s*(La Comisión asignará .*?distribuidos así:)", seg[k])
        _need(m, f"art. 5 inciso {k}")
        inc[k] = m.group(1)
    l685 = C253.page_text("ley_0685_2001")
    m = re.search(r"ARTÍCULO 359\. El primer inciso del parágrafo único del artículo 5 ?o de la Ley 141 de 1994 quedará "
                  r"así: (La Comisión asignará el trece punto cinco .*?distribuidos así:) A este parágrafo se le adiciona "
                  r"el numeral 18", l685)
    _need(m and m.group(1)[:-len(" así:")] in seg["Ley 685 de 2001"], "art. 5 Ley 685 art. 359")
    inc["Ley 685 de 2001"] = m.group(1)
    num = {}
    for k, n, end in (("Ley 344 de 1996", "17", "Zapatoza."), ("Ley 619 de 2000", "17", "caños."),
                      ("Ley 685 de 2001", "18", "Zapatoza.")):
        m = re.search(r"<Numeral adicionado por el artículo \d+ de la " + k + r"\. El (?:nuevo )?texto es el siguiente:>\s*"
                      r"(El cero punto .*?" + re.escape(end) + ")", seg[k])
        _need(m, f"art. 5 numeral {n} {k}")
        num[k] = f"{n}. {m.group(1)}"
    h = H._hist(act, "art-0005")
    _need([(d, c) for d, _, c in h] == [("1994-06-30", None), ("1996-12-31", ["ley-344-1996"]), (L619_DAY, [L619]),
                                        ("2001-09-08", ["ley-685-2001"]), ("2002-07-25", ["ley-756-2002"])]
          and h[0][1] == [H.PH], f"art. 5 {H._shape(h)}")
    now, b96 = h[-1][1], h[1][1]
    head = now[:9]
    _need(b96[:9] == head and head[-1].startswith("8. ") and now[9].startswith("PARÁGRAFO."), "art. 5 head")
    i0 = b96.index(next(l for l in b96 if l.startswith("PARÁGRAFO. La Comisión asignará el doce punto seiscientos")))
    i1 = b96.index(next(l for l in b96 if l.startswith("Para los efectos del artículo 3o. parágrafo 5o.")))
    p94 = b96[i0:i1 + 1]
    o = _norm(seg["orig"])
    _need(i0 == 9 and len(p94) == 19 and [l.split(".")[0] for l in p94[1:17]] == [str(i) for i in range(1, 17)]
          and all(_norm(l) in o for l in p94), "art. 5 original parágrafo")
    _need(num["Ley 344 de 1996"] in b96 and num["Ley 685 de 2001"] in h[3][1], "art. 5 engine numerals")
    nums, close = p94[1:17], p94[17:]

    def par(k, extra):
        return head + [f"PARÁGRAFO. {inc[k]}"] + nums + extra + close
    _apply(act, "art-0005", [(None, head + p94, None),
                             ("1996-12-31", par("Ley 344 de 1996", [num["Ley 344 de 1996"]]), "ley-344-1996"),
                             (L619_DAY, par("Ley 619 de 2000", [num["Ley 619 de 2000"]]), L619),
                             ("2001-09-08", par("Ley 685 de 2001", [num["Ley 619 de 2000"], num["Ley 685 de 2001"]]),
                              "ley-685-2001"),
                             (C737_END, par("Ley 685 de 2001", [num["Ley 344 de 1996"], num["Ley 685 de 2001"]]),
                              E_reg(C737)),
                             ("2002-07-25", now, "ley-756-2002")])
    H._done(T141, fix_5)


def fix_16(act):
    """art. 16 (royalty rates): rewritten by Ley 508 de 1999 (30 July 1999), by Decreto 955 de 2000 (26 May 2000), by
    Ley 619 de 2000 (20 October 2000) and by Ley 756 de 2002; the page gives the original text and Ley 619's and Ley
    756's, not Ley 508's or the decree's (placeholders). Sentencia C-557 de 2000 (16 May 2000) struck Ley 508 de 1999
    and Sentencia C-1403 de 2000 (19 October 2000) struck Decreto 955 de 2000, each as a whole: the original text is back
    on each ruling's day; Ley 619's words then stand until Sentencia C-737 de 2001's deferral ended on 20 June 2002, the
    original back that day until Ley 756 de 2002 (25 July 2002). Sentencia C-845 de 2000, which the notes also name,
    held words of the original parágrafo 2o. EXEQUIBLE (no change). The engine had the article out from the decree's
    day and again from the ruling of 11 July 2001."""
    u = _u(16)
    jv, nv = H._jv(u), H._nv(u)
    _need("El Decreto 955 de 2000 fue declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1403-00 del 19 "
          "de octubre de 2000" in jv and "La Ley 508 de 1999 fue declarada INEXEQUIBLE por la Corte Constitucional, "
          "mediante sentencia C-557-2000 del 16 de mayo de 2000" in jv and C737_QUOTE in jv and "Aparte subrayado del "
          "parágrafo 2o. declarado EXEQUIBLE por la Corte Constitucional, mediante Sentencia C-845-00" in jv, "art. 16 JV")
    _need("Artículo modificado por el artículo 60 del Decreto 955 de 2000" in nv and "Artículo modificado por el artículo "
          "72 de la Ley 508 de 1999" in nv, "art. 16 NV")
    h = H._hist(act, "art-0016")
    _need([(d, c, None if b is None else (b == [H.PH])) for d, b, c in h] == [
        ("1994-06-30", None, False), ("1999-07-30", ["ley-508-1999"], True), ("2000-05-26", ["dec-955-2000"], None),
        (L619_DAY, [L619], False), (C737_RULING_DAY, [C737], None), ("2002-07-25", ["ley-756-2002"], False)],
          f"art. 16 {H._shape(h)}")
    orig = h[0][1]
    o = _orig_seg(u)
    _need(len(o) == 1 and orig[0].startswith("REGALÍAS DERIVADAS DE LA EXPLOTACIÓN DE HIDROCARBUROS")
          and all(_norm(l) in o[0] for l in orig[1:]), "art. 16 original")
    c557 = H.E.add_court("C-557-00", "2000-05-16", "c-557_2000.html")
    c1403 = H.E.add_court("C-1403-00", "2000-10-19", "c-1403_2000.html")
    _apply(act, "art-0016", [(None, orig, None), ("1999-07-30", [H.PH], "ley-508-1999"), ("2000-05-16", orig, c557),
                             ("2000-05-26", [H.PH], "dec-955-2000"), ("2000-10-19", orig, c1403),
                             (L619_DAY, h[3][1], L619), (C737_END, orig, E_reg(C737)), ("2002-07-25", h[5][1], "ley-756-2002")])
    H._done(T141, fix_16)


C580_SPANS = ("irá en calidad de depósito a un fondo especial en el Departamento de Sucre",
              "irá en calidad de depósito a un fondo especial en el Departamento de Córdoba",
              "dentro de los diez (10) días siguientes a su recibo")


def fix_29(act):
    """art. 29 (the ports' share), parágrafo 1o.: as for art. 1, the engine had laid the parágrafo as enacted over
    today's lines of it (Ley 756 de 2002's), and Ley 619 de 2000's parágrafo (the box) over them too, so every version
    before 25 July 2002 held both: those lines now arrive with
    Ley 756 de 2002. Sentencia C-580 de 1999 (11 August 1999) struck, in the parágrafo as enacted, the words the box shows
    struck ('irá en calidad de depósito a un fondo especial en el Departamento de Sucre'; 'irá en calidad de depósito a
    un fondo especial en el Departamento de Córdoba' and 'dentro de los diez (10) días siguientes a su recibo' in the
    Córdoba line): out that day, credited to the ruling (the engine had dropped them from no version). Ley 619 de 2000's
    parágrafo then stands until Sentencia C-737 de 2001's deferral ended on 20 June 2002, when the parágrafo as the 1999
    ruling left it is back, until Ley 756 de 2002 (the engine had a placeholder from the ruling of 11 July 2001). Ley 2056 de 2020, art. 26, which the notes name as modifying
    parágrafo 2o., left its words as Ley 1530 de 2012 wrote them (no version)."""
    u = _u(29)
    _need("Apartes tachados del texto original del parágrafo 1o. declarados INEXEQUIBLES por la Corte Constitucional "
          "mediante Sentencia C-580-99 de 11 de agosto de 1999" in H._jv(u) and C737_QUOTE in H._jv(u), "art. 29 JV")
    _need("Parágrafo modificado por el artículo 26 de la Ley 2056 de 2020" in H._nv(u), "art. 29 NV 2056")
    h = H._hist(act, "art-0029")
    want = [None, ["c-299-99"], [L619], [C737], ["ley-756-2002"], ["dec-4923-2011"], ["ley-1530-2012"]]
    _need([c for _, _, c in h] == want and h[3][0] == C737_RULING_DAY and h[3][1] == [H.PH], f"art. 29 {H._shape(h)}")
    today, orig = set(h[-1][1]), _orig_seg(u)
    bl = [None if b == [H.PH] else _blocks(b) for _, b, _ in h]
    _need(all(len(b) == 4 for b in bl if b), f"art. 29 blocks {H._shape(h)}")
    tails = []
    for i in (0, 1):
        bl[i][1], tail = _cut_mix(bl[i][1], today, orig)
        tails.append(tail)
    _need(tails[0] and tails[0] == tails[1] and tails[0] == bl[4][1][len(bl[4][1]) - len(tails[0]):], "art. 29 tails")
    _need(all(bl[2][k] == bl[1][k] for k in range(4) if k != 1), "art. 29 Ley 619")
    p619 = [a for a, _ in _struck_paras(u, "Texto modificado por la Ley 619 de 2000:")]
    _need(bl[2][1][:len(p619)] == p619 and bl[2][1][len(p619):] == bl[4][1][1:], "art. 29 Ley 619 block")
    bl[2][1] = p619
    sp = _struck_paras(u, "Texto original de la Ley 141 de 1994")
    p1 = bl[1][1]
    _need([a for a, _ in sp] == p1, f"art. 29 original box {len(sp)} {len(p1)}")
    gone = [b for a, b in sp]
    _need([s for s in C580_SPANS if any(s in a and s not in b for a, b in sp)] == list(C580_SPANS), "art. 29 spans")
    c580 = H.E.add_court("C-580-99", "1999-08-11", "c-580_1999.html")
    t99, t580 = _flat(bl[1]), _flat([bl[1][0], gone] + bl[1][2:])
    _apply(act, "art-0029", [(None, _flat(bl[0]), None), ("1999-05-05", t99, "c-299-99"), ("1999-08-11", t580, c580),
                             (L619_DAY, _flat(bl[2]), L619), (C737_END, t580, E_reg(C737))]
           + [(d, b, c[0]) for d, b, c in h[4:]])
    H._done(T141, fix_29)


def fix_3(act):
    """art. 3 (which projects are eligible): the engine had a placeholder from 1994 (the page prints today's text and,
    in its box, only the original inciso 1o. and parágrafos 2o. and 4o.). As enacted: the original inciso 1o. (the box),
    parágrafos 1o., 3o. and 5o. as printed today, parágrafos 2o. and 4o. as enacted (the boxes); Ley 344 de 1996 (31
    December 1996) rewrote inciso 1o. (art. 6, the two paragraphs printed today) and added the closing parágrafo (art. 4).
    Decreto 1178 de 1999, art. 22 (29 June 1999), repealed parágrafo 1o. and art. 6 of Ley 344 de 1996, i.e. inciso 1o.
    as it then read (no earlier text revives on a repeal): both out that day, the article's epigraph left standing;
    Sentencia C-722 de 1999 (29 September 1999) struck the decree, so both are back that day (as Ley 344 art. 6 in
    99zzzzzzzz-094-batch94); then Ley 756 de 2002 (25 July 2002) rewrote parágrafos 2o. and 4o."""
    u = _u(3)
    nv = H._nv(u)
    _need("Artículo 6 de la Ley 344 de 1996 fue derogado por el artículo 22 del Decreto 1178 de 1999" in nv and "Parágrafo "
          "derogado por el artículo 22 del Decreto 1178 de 1999" in nv and "Inciso 1o. modificado por el artículo 6o. de la "
          "Ley 344 de 1996" in nv and "Parágrafo adicionado por el artículo 4o. de la Ley 344 de 1996" in nv
          and "Sentencia C-722-99 del 29 de Septiembre de 1999" in H._jv(u), "art. 3 notes")
    m = re.search(r"Texto original de la Ley 141 de 1994:\s*<INCISO 1o\.>\s*(Para que un proyecto sea elegible .*?ambiental\.)",
                  _box(u))
    _need(m, "art. 3 box inciso")
    h = H._hist(act, "art-0003")
    _need([(d, c) for d, _, c in h] == [("1994-06-30", None), ("1996-12-31", ["ley-344-1996"]),
                                        ("2002-07-25", ["ley-756-2002"])] and h[0][1] == [H.PH], f"art. 3 {H._shape(h)}")
    t96 = h[1][1]
    epi = "ELEGIBILIDAD DE LOS PROYECTOS."
    _need(len(t96) == 8 and t96[0].startswith(epi + " Para que un proyecto regional") and t96[1].startswith("Estos proyectos")
          and t96[2].startswith("PARÁGRAFO 1o.") and t96[7].startswith("PARÁGRAFO. Tratándose"), "art. 3 1996 text")
    o = _orig_seg(u)
    _need(all(any(_norm(l) in x for x in o) for l in (t96[3], t96[5])), "art. 3 original parágrafos")
    t94 = [f"{epi} {m.group(1)}"] + t96[2:7]
    t99 = [epi] + t96[3:]
    _apply(act, "art-0003", [(None, t94, None), ("1996-12-31", t96, "ley-344-1996"), ("1999-06-29", t99, "dec-1178-1999"),
                             ("1999-09-29", t96, "c-722-99"), ("2002-07-25", h[2][1], "ley-756-2002")])
    H._done(T141, fix_3)


def note_149(act):
    """arts. 7 to 12 (the Comisión Nacional de Regalías): the notes say the Comisión was suppressed by Decreto 149 de
    2004 (Diario Oficial No. 45.443 of 27 January 2004) and that, by art. 52 of Decreto 195 de 2004, references to it are
    read as references to the Departamento Nacional de Planeación. Neither decree repealed or rewrote words of Ley 141 de
    1994, and the page prints the articles as in force: their words stand (no version)."""
    for num in range(7, 13):
        nv = H._nv(_u(num))
        _need("La Comisión Nacional de Regalías fue suprimida por el Decreto 149 de 2004" in nv
              and "ARTÍCULO 52. REFERENCIAS NORMATIVAS" in nv, f"art. {num}: Decreto 149 note")
    H._done(T141, note_149)


L756_PAGE = "ley_0756_2002"
L756_ARTS = {35: "20", 43: "21"}
# The Ley 141 page's headings of arts. 35 and 43 today (the 1994 epigraph words, art. 43's with Ley 756's tail added).
PAGE_HEADS = {35: "DISTRIBUCIÓN DE LAS REGALÍAS DERIVADAS DE LA EXPLOTACIÓN DE PIEDRAS PRECIOSAS.",
              43: "DISTRIBUCIÓN DE LAS COMPENSACIONES MONETARIA DERIVADAS DE LA EXPLOTACIÓN DE LAS ESMERALDAS Y DEMÁS "
                  "PIEDRAS PRECIOSAS."}
BODY_43 = "Las compensaciones monetarias derivadas de la explotación de esmeraldas y demás piedras preciosas se distribuirán así:"


def l756_line(num):
    """The words Ley 756 de 2002 (art. 20 for art. 35, art. 21 for art. 43) gave the article before its distribution
    table, as one line, as Ley 756's own text prints them (an epigraph in capitals alone would read as the remnant of
    a struck article: B6.drop_epigraph_only)."""
    u = H.B23._unit(L756_PAGE, L756_ARTS[num])
    ps = [H.E.tidy(H.E.plain(it[1])) for it in u["items"] if it[0] == "p"]
    _need(ps and ps[0] == f"El artículo {num} de la Ley 141 de 1994{',' if num == 43 else ''} quedará así:"
          and len(ps) > 1 and ps[1].startswith(f'"Artículo {num}. Distribución de las '), f"Ley 756 art. {L756_ARTS[num]}: {ps[:2]}")
    words = ps[1][len(f'"Artículo {num}. '):]
    epi, _, rest = words.partition(". ")
    epi = epi.rstrip(".")
    _need(epi.endswith("esmeraldas y demás piedras preciosas") and rest == ("" if num == 35 else BODY_43),
          f"Ley 756 art. {L756_ARTS[num]} words: {words}")
    return f"{epi}." + (f" {rest}" if rest else "")


def page_today_756(num, lines):
    """For the verifier: the Ley 141 page's lines for art. 35 (none: its words today are a table, left out) and art. 43
    (its heading as PAGE_HEADS gives), read with Ley 756's own words (l756_line)."""
    if num == 35:
        _need(lines == [], f"art. 35 page lines {lines}")
    else:
        _need(lines == [f"{PAGE_HEADS[43]} {BODY_43}"], f"art. 43 page lines {lines}")
    return [l756_line(num)]


def fix_35_43(act):
    """arts. 35 and 43 (distribution of the royalties and compensations from emeralds and other precious stones): Ley
    756 de 2002 (25 July 2002), arts. 20 and 21, rewrote both; each new article is a heading (art. 43: with one sentence)
    over a distribution table, and tables are left out of the text, as everywhere in the corpus. From 25 July 2002 the
    articles read the words Ley 756 wrote before its tables (art. 35: 'Distribución de las regalías derivadas de la
    explotación de esmeraldas y demás piedras preciosas.'; art. 43: 'Distribución de las compensaciones monetarias
    derivadas de la explotación de esmeraldas y demás piedras preciosas. Las compensaciones monetarias ... se
    distribuirán así:'), as Ley 756's own text prints them; the Ley 141 page's own headings, in capitals, keep words of
    the 1994 epigraphs ('PIEDRAS PRECIOSAS' alone in art. 35; 'MONETARIA' and 'DE LAS ESMERALDAS' in art. 43) where Ley
    756's text reads otherwise, and Ley 756's text is followed. Decreto 1660 de 2008 corrected only a municipality's name
    in the tables ('Guvetá' to 'Guayatá'): it changes no words here and makes no version. The engine had held a
    placeholder from 2002 to 2008 in both articles and dropped art. 35 after 2008 (its page text is only the table)."""
    for num in (35, 43):
        u, key = _u(num), _key(num)
        pt = " ".join(H.E.plain(it[1]) for it in u["items"] if it[0] == "p")
        _need(f"Artículo modificado por el artículo {L756_ARTS[num]} de la Ley 756 de 2002. El nuevo texto es el siguiente" in pt
              and f'Referencia del municipio "Guvetá" corregida por "Guayatá" por el artículo {1 if num == 35 else 2} del '
              f"Decreto 1660 de 2008" in pt, f"art. {num} markers")
        h = H._hist(act, key)
        days = [d for d, _, _ in h]
        _need(days[-2:] == ["2002-07-25", "2008-07-20"] and h[-2][1] == [H.PH] and h[-2][2] == ["ley-756-2002"]
              and h[-1][2] == ["dec-1660-2008"] and (h[-1][1] is None if num == 35 else
                                                    h[-1][1] == [f"{PAGE_HEADS[43]} {BODY_43}"]),
              f"art. {num} shape {H._shape(h)}")
        tl = [(None, h[0][1], None)] + [(d, b, c[0]) for d, b, c in h[1:-2]] + [("2002-07-25", [l756_line(num)], "ley-756-2002")]
        _need(all(c and len(c) == 1 for _, _, c in h[1:-2]), f"art. {num} credits {H._shape(h)}")
        _apply(act, key, tl)
    vs = act["versions"]
    i = next(i for i, v in enumerate(vs) if v["from"] == "2008-07-20")
    prev = next(v for v in reversed(vs[:i]) if "units" in v)
    _need(not vs[i]["credits"] and vs[i].get("units", prev["units"]) == prev["units"], f"2008-07-20 version {vs[i]['credits']}")
    del vs[i]
    H._done(T141, fix_35_43)


H.FIXES[S141] = [fix_c737, fix_9, fix_1, fix_3, fix_5, fix_16, fix_29, fix_21_22, fix_struck_lines, note_149, fix_35_43]
