"""Hand-set histories for batch 74 (Leyes 1608 de 2013, 1949 de 2019, 1966 de 2019), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L1608, T1608 = "ley_1608_2013", "Medidas para mejorar la liquidez y el uso de algunos recursos del sector salud (Ley 1608 de 2013)"


def fix_1608_7(act):
    """art. 7 (Ley 1438 de 2011 art. 50, quoted): the page prints its text after the marker '<Artículo derogado el a partir
    del 31 de diciembre de 2019 por el artículo 336 de la Ley 1955 de 2019>' (its Notas de Vigencia: 'Artículo derogado a
    partir del 31 de diciembre de 2019 por el artículo 336 de la Ley 1955 de 2019'), with no earlier-text box; the engine
    read the marker as the day the words came in (Ley 1955's own day, 25 May 2019, the placeholder before) and kept them
    to today. It reads as printed from the act's first day and leaves on 31 December 2019, credited to Ley 1955 de 2019."""
    B23 = H.B23
    u = B23._unit(L1608, "7")
    B23._need("Artículo derogado a partir del 31 de diciembre de 2019 por el artículo 336 de la Ley 1955 de 2019" in H._nv(u)
              and not any(it[0] == "box" and it[1] == "Legislación Anterior" for it in u["items"]), "L1608 art. 7 note")
    key = "art-0007"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2013-01-02", None), ("2019-05-25", ["ley-1955-2019"])] and h[0][1] == [H.PH],
              f"L1608 art. 7 {H._shape(h)}")
    B23._need(h[1][1][0] == "El artículo 50 de la Ley 1438 de 2011 quedará así:", "L1608 art. 7 text")
    H._set(act, key, H._label(act, key), [(None, h[1][1], None), ("2019-12-31", None, "ley-1955-2019")])
    B23._forget(L1608, key)
    H._done(T1608, fix_1608_7)


H.FIXES.setdefault("liquidez-sector-salud", []).append(fix_1608_7)
