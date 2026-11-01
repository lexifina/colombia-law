"""Hand-set histories for batch 91 (Leyes 790 de 2002 and 1444 de 2011), installed by hand_fixes.install(); each
checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L790, T790, S790 = ("ley_0790_2002", "Renovación de la administración pública (Ley 790 de 2002)",
                    "renovacion-de-la-administracion-publica-2002")
L1444, T1444, S1444 = ("ley_1444_2011", "Escisión de ministerios y facultades extraordinarias (Ley 1444 de 2011)",
                       "escision-de-ministerios-2011")


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


def _need(c, what):
    H.B23._need(c, what)


def _u(page, num):
    return H.B23._unit(page, num)


def _p0(u):
    return H.E.plain(next(it[1] for it in u["items"] if it[0] == "p"))


def _units_on(act, days):
    """A version on one of `days` that carries no units (it changed no words) gets a copy of the units before it, so a
    text set for that day lands on it (set_history skips versions without units; hf89 rule)."""
    full = None
    for v in act["versions"]:
        if "units" in v:
            full = v["units"]
        elif v["from"] in days:
            v["units"] = dict(full)
            full = v["units"]


def _apply(act, page, key, tl):
    _units_on(act, {d for d, _, _ in tl[1:]})
    H._set(act, key, H._label(act, key), tl)
    H.B23._forget(page, key)


# ------------------------------------------------------------------------------------------------- Ley 790 de 2002

def fix_790_13(act):
    """art. 13 (the time the chapter's benefits apply): the page shows struck its last words ('y hasta el vencimiento de
    las facultades extraordinarias que se confieren en la presente ley') under the marker 'Aparte tachado derogado
    tácitamente por el artículo 8, literal D., último y penúltimo inciso, de la Ley 812 de 2003, según lo establece la
    Corte Constitucional mediante Sentencia C-991-04' (the ruling itself was an inhibition for want of object). As for the
    Código Civil's tacit repeals (fix_tacit_cc.py), the words stand from the act's first day and go from the in-force
    day of the act the page names, Ley 812 de 2003 (27 June 2003, its art. 137: from its promulgation), credited to it
    (the engine had kept them in every version)."""
    E = H.E
    u = _u(L790, "13")
    _need(E.markers(next(it[1] for it in u["items"] if it[0] == "p"))[:1]
          == ["Aparte tachado derogado tácitamente por el artículo 8, literal D., último y penúltimo inciso, de la Ley 812 "
              "de 2003, según lo establece la Corte Constitucional mediante Sentencia C-991-04"], "L790 art. 13 marker")
    _need("fue derogado tácitamente por el artículo 8, literal D., último y penúltimo inciso, de la Ley 812 de 2003"
          in H._jv(u), "L790 art. 13 JV")
    before, after = H._printed(u, keep_struck=True), H._printed(u)
    _need(len(before) == len(after) == 1 and before[0].endswith("orden nacional, y hasta el vencimiento de las facultades "
          "extraordinarias que se confieren en la presente ley.") and after[0].endswith("orden nacional,."),
          f"L790 art. 13 lines {after}")
    h = H._hist(act, "art-0013")
    _need([(d, c) for d, _, c in h] == [("2002-12-27", None)] and h[0][1] == before, f"L790 art. 13 {H._shape(h)}")
    k = E.register("ley-812-2003")
    _need(E.law_day(k) == "2003-06-27", f"Ley 812 de 2003 day {E.law_day(k)}")
    _apply(act, L790, "art-0013", [(None, before, None), ("2003-06-27", after, k)])
    H._done(T790, fix_790_13)


# ------------------------------------------------------------------------------------------------ Ley 1444 de 2011

C161, C161_DAY, C161_END = "C-161-24", "2024-05-08", "2026-06-20"


def fix_1444_17(act):
    """art. 17 (number and order of the ministries): Ley 2281 de 2023 art. 15 (4 January 2023) gave it nineteen
    ministries, the last '19. Ministerio de Igualdad y Equidad.'. The page shows those words struck, followed by an
    unclosed note '<Ministerio liquidado mediante el Decreto 626 de 2026', and its Notas de Vigencia say Sentencia
    C-161-24 (press release of 8 May 2024) struck Ley 2281 de 2023 and deferred its effects for two legislatures from 20
    July 2024: 'Una vez culmine la legislatura 2025-2026, la Ley 2281 de 2023 dejará de producir efectos
    definitivamente'. The legislature ends on 20 June (Constitución art. 138). As for Sentencia C-253 de 2010's deferral
    (fix_c253_deferral.py), the words stand until the deferral's last day and go on 20 June 2026, credited to the ruling;
    Decreto 626 de 2026 (liquidating the ministry, in force from 23 June 2026) came after that day and makes no version.
    The number '19.' the page prints unstruck is kept as the item's label (hf89 rule for struck added items), and the
    unclosed note is not law text. The engine had dropped the struck words from every version and kept the note as
    text. The rest of Ley 2281's wording ('diecinueve') stays to today, as the page prints it."""
    E = H.E
    u = _u(L1444, "17")
    nv = H._nv(u)
    _need("declarada INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-161-24 según Comunicado de Prensa de 8 de "
          "mayo de 2024" in nv and "Difiere los efectos de la decisión, por el término de dos (2) legislaturas, contadas a "
          "partir del 20 de julio 2024. Una vez culmine la legislatura 2025-2026, la Ley 2281 de 2023 dejará de producir "
          "efectos definitivamente" in nv and "Rige a partir del 23 de junio de 2026" in nv, "L1444 art. 17 NV")
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    _need(E.plain(ps[-1]) == "19. Ministerio de Igualdad y Equidad. <Ministerio liquidado mediante el Decreto 626 de 2026"
          and "<S>" in ps[-1], f"L1444 art. 17 last item {E.plain(ps[-1])!r}")
    h = H._hist(act, "art-0017")
    _need([(d, c) for d, _, c in h] == [("2011-05-04", None), ("2019-07-11", ["ley-1967-2019"]),
                                        ("2021-12-06", ["ley-2162-2021"]), ("2023-01-04", ["ley-2281-2023"])]
          and h[3][1][-1] == "19.. <Ministerio liquidado mediante el Decreto 626 de 2026", f"L1444 art. 17 {H._shape(h)}")
    t23 = h[3][1][:-1] + ["19. Ministerio de Igualdad y Equidad."]
    t26 = h[3][1][:-1] + ["19."]
    k = E.add_court(C161, C161_DAY, "c-161_2024.html")
    _apply(act, L1444, "art-0017", [(None, h[0][1], None), ("2019-07-11", h[1][1], "ley-1967-2019"),
                                    ("2021-12-06", h[2][1], "ley-2162-2021"), ("2023-01-04", t23, "ley-2281-2023"),
                                    (C161_END, t26, k)])
    H._done(T1444, fix_1444_17)


H.FIXES[S790] = [fix_790_13]
H.FIXES[S1444] = [fix_1444_17]
