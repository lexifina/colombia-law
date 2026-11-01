"""Hand-set histories for batch 111 (Ley 2094 de 2021), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L2094, S2094 = "ley_2094_2021", "reforma-del-codigo-general-disciplinario-2021"
T2094 = "Reforma del Código General Disciplinario (Ley 2094 de 2021)"
LAW2094 = "ley-2094-2021"
FOLDED: list = []


def fix_stages(act):
    """Ley 2094 de 2021, art. 73 (art. 265 of the Código General Disciplinario as it rewrites it): nine months after
    promulgation for the act, art. 1 from promulgation (par. 1o.; the page's marker on art. 1: 'En lo relativo a las
    funciones jurisdiccionales entrará a regir a partir del 29 de junio de 2021'), art. 7 thirty months after it (par.
    2o.). The first version, of 29 June 2021, holds art. 1; every other article except art. 7 is added on 29 March 2022
    and art. 7 on 29 December 2023, credited to the act (phase2/late.py), the days the Código General Disciplinario part
    gives these changes. Decreto 1656 de 2021's corrections (6 December 2021) to articles that applied from 29 March
    2022 arrive with them that day, credited to the act and the decree."""
    import late
    E, P, B23 = H.E, H.P, H.B23
    pub = act["versions"][0]["from"]
    nine, thirty = E.add_months(pub, 9), E.add_months(pub, 30)
    B23._need((pub, nine, thirty) == ("2021-06-29", "2022-03-29", "2023-12-29"), f"L2094 days {pub} {nine} {thirty}")
    u1 = H.B23._unit(L2094, "1")
    p0 = next(it[1] for it in u1["items"] if it[0] == "p")
    B23._need("entrará a regir a partir del 29 de junio de 2021" in E.plain(p0), "L2094 art. 1 marker")
    nums = [E.label_num(u["label"] or "") for u in P.doc_units(L2094)[1:]]
    nums = [n for n in nums if n]
    B23._need(nums == [str(i) for i in range(1, 76)], f"L2094 articles {nums}")
    # Decreto 1656 de 2021 (Diario Oficial No. 51.880 of 6 December 2021) corrected errors in the act before those
    # articles applied: its corrections arrive with them, credited to the act and the decree (as the Código General
    # Disciplinario part shows them from 29 March 2022).
    late.FOLDED.clear()
    late.late_start(act, [n for n in nums if n not in ("1", "7")], nine, LAW2094, L2094, P, E, B23, fold=("dec-1656-2021",))
    late.late_start(act, ["7"], thirty, LAW2094, L2094, P, E, B23)
    B23._need(all(f.endswith(": Decreto 1656 de 2021") for f in late.FOLDED), f"L2094 folded {late.FOLDED}")
    FOLDED.extend(late.FOLDED)
    late.FOLDED.clear()
    H._done(T2094, fix_stages)


H.FIXES[S2094] = [fix_stages]
