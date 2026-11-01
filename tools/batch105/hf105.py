"""Hand-set histories for batch 105 (Leyes 689 de 2001 and 225 de 1995), installed by hand_fixes.install(); each
checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L689, S689 = "ley_0689_2001", "reforma-de-servicios-publicos-2001"
T689 = "Reforma de la Ley de Servicios Públicos Domiciliarios (Ley 689 de 2001)"


def note_689_23(act):
    """Ley 689 de 2001, art. 23 (margen de seguridad del GLP): the page's Notas de Vigencia say that the margin 'se
    eliminará a partir del 31 de diciembre de 2010, por el artículo 62, inciso 2o. de la Ley 1151 de 2007' (Plan Nacional
    de Desarrollo 2006-2010; kept in force by Ley 1450 de 2011 art. 276 and Ley 1753 de 2015 art. 267). Ley 1151 orders the
    regulator to fold the cylinders' costs into the tariff and ends the margin: a rule of its own, which repeals none of
    art. 23's words; the page prints the article in force under '<Ver Notas de Vigencia>'. No version."""
    u = H.B23._unit(L689, "23")
    H.B23._need("se eliminará a partir del 31 de diciembre de 2010, por el artículo 62, inciso 2o. de la Ley 1151 de 2007"
                in H._nv(u), "L689 art. 23 NV")
    h = H._hist(act, "art-0023")
    H.B23._need(len(h) == 1, f"L689 art. 23 shape {H._shape(h)}")
    H._done(T689, note_689_23)


H.FIXES[S689] = [note_689_23]
