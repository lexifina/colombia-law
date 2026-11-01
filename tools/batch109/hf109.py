"""Hand-set histories for batch 109 (Ley 712 de 2001), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L712, S712 = "ley_0712_2001", "reforma-del-procedimiento-laboral-2001"
T712 = "Reforma del Código Procesal del Trabajo (Ley 712 de 2001)"


def note_ghost(act):
    """Ley 712 de 2001: the page follows each chapter heading after the first with an empty anchor named 'CAPITULO I'
    (a navigation slip with no words); read as a heading it blanked the chapter headings, so the empty anchors are left
    out and the chapters read as the page prints them ('CAPITULO II. COMPETENCIA.' ...)."""
    n = sum(H.D.GHOST_HITS.values())
    H.B23._need(n == 12, f"L712 empty anchors {H.D.GHOST_HITS}")
    t = act["versions"][0]["units"]["titulos"]["text"]
    H.B23._need("### \n" not in t and "CAPITULO II. COMPETENCIA." in t, "L712 titulos")
    H._done(T712, note_ghost)


H.FIXES[S712] = [note_ghost]
