"""Hand-set histories for batch 96 (Leyes 1142 de 2007 and 1185 de 2008), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L1142, T1142 = "ley_1142_2007", "Ley 1142 de 2007"
# Art. 16 (CPP art. 237 as rewritten): 'sólo' struck by Sentencia C-025-09 (press release of 27 and 28 January 2009; the
# corpus dates C-025-09 on 27 January, 80-batch3's CPP art. 237); the engine had dropped the word from every version.
H.STRUCK[L1142] = [("16", "C-025-09", "2009-01-27", "c-025_2009.html",
                    "salvo el aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-025-09 "
                    "según Comunicado de Prensa de la Sala Plena de 27 y 28 de enero de 2009")]
H.FIXES.setdefault("convivencia-y-seguridad-ciudadana-2007", []).append(H.fix_struck(L1142, T1142))
