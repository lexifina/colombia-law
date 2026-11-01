"""Hand-set histories for batch 110 (Ley 2430 de 2024), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L2430, S2430 = "ley_2430_2024", "reforma-de-la-administracion-de-justicia-2024"
T2430 = "Reforma de la Ley Estatutaria de la Administración de Justicia (Ley 2430 de 2024)"


def note_prior_review(act):
    """Ley 2430 de 2024 (a statutory law): every ruling its page names is Sentencia C-134-23 (3 May 2023), the Court's
    prior review of the bill (Proyecto de Ley Estatutaria 295 de 2020 Cámara - 475 de 2021 Senado) before it was
    sanctioned; the act as promulgated already carries its outcome, so the ruling makes no version, and the 'Texto del
    Proyecto de Ley Anterior' boxes (the bill's words) are not law and are not read. The act has one version, from its
    promulgation (Diario Oficial No. 52.904 of 9 October 2024, art. 93)."""
    t = " ".join(H._jv(u) for u in H.P.doc_units(L2430)[1:])
    rulings = set(re.findall(r"Sentencia (C-\d+-\d+)", t))
    H.B23._need(rulings == {"C-134-23"} and "revisión de constitucionalidad del Proyecto de Ley Estatutaria 295 de 2020" in t,
                f"L2430 rulings {rulings}")
    H.B23._need([v["from"] for v in act["versions"]] == ["2024-10-09"], "L2430 versions")
    H._done(T2430, note_prior_review)


H.FIXES[S2430] = [note_prior_review]
