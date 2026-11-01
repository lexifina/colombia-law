"""Hand-set histories for batch 72 (Leyes 310 de 1996, 1383 de 2010, 1696 de 2013), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L310, T310 = "ley_0310_1996", "Sistemas de servicio público urbano de transporte masivo de pasajeros, modificación de la Ley 86 de 1989 (Ley 310 de 1996)"
L1383, T1383 = "ley_1383_2010", "Reforma del Código Nacional de Tránsito (Ley 1383 de 2010)"
L1696, T1696 = "ley_1696_2013", "Sanciones por conducción bajo el influjo del alcohol u otras sustancias psicoactivas (Ley 1696 de 2013)"


def _la(u, head, first=None):
    """The lines of the earlier-text block headed `head` (the only one whose first line starts with `first`), the
    publisher's leading '<Inciso N.>' label out."""
    B23, E = H.B23, H.E
    out = []
    for b in B23._boxes(u, "Legislación Anterior"):
        for blk in E.la_blocks(b):
            if blk["head"].rstrip(" :").startswith(head):
                ls = [E.tidy(re.sub(r"^<[^<>]*>\s*", "", x)) for x in E.block_text(blk["paras"], False)]
                ls = [x for x in ls if x]
                if ls and (first is None or ls[0].startswith(first)):
                    out.append(ls)
    B23._need(len(out) == 1, f"box {head!r} {first!r}: {len(out)}")
    return out[0]


def _one_line(lines, start):
    k = [i for i, x in enumerate(lines) if x.startswith(start)]
    H.B23._need(len(k) == 1, f"line {start!r}")
    return k[0]


def _units_on_day(act, day):
    vs = act["versions"]
    for i, v in enumerate(vs):
        if v["from"] == day and "units" not in v:
            v["units"] = dict(next(p for p in reversed(vs[:i]) if "units" in p)["units"])


def fix_310_3(act):
    """art. 3: its only note says that Decreto Legislativo 575 de 2020 art. 4 modified 'transitoriamente' the article, but
    the words it quotes modify Ley 1955 de 2019's art. 100, which rewrote art. 2 of this act, not art. 3 (and only for an
    emergency of undated end, which the corpus leaves out); no note gives art. 3 any other change. It reads as the page
    prints it from the act's first day; the engine had the placeholder until 2020 and credited the decree."""
    B23 = H.B23
    u = B23._unit(L310, "3")
    nv = H._nv(u)
    B23._need("Artículo modificado transitoriamente por el artículo 4 del Decreto Legislativo 575 de 2020" in nv
              and "modifíquese el artículo 100 de la Ley 1955 de 2019" in nv and "Modifíquese el artículo 2o de la Ley 310 de 1996"
              in nv and not any(it[0] == "box" and it[1] == "Legislación Anterior" for it in u["items"]), "L310 art. 3 note")
    key = "art-0003"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1996-08-12", None), ("2020-04-15", ["dec-575-2020"])] and h[0][1] == [H.PH],
              f"L310 art. 3 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, h[1][1], None)])
    B23._forget(L310, key)
    H._done(T310, fix_310_3)


H.FIXES.setdefault("transporte-masivo-1996", []).append(fix_310_3)
