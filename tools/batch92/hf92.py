"""Hand-set histories for batch 92 (Leyes 679 y 681 de 2001), installed by hand_fixes.install(); each checks the page
first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L681, T681, S681 = ("ley_0681_2001", "Concesiones de combustibles en las zonas de frontera (Ley 681 de 2001)",
                    "combustibles-zonas-de-frontera-2001")
A116 = ("La derogatoria de los artículos 10, 11 y el parágrafo del artículo 12 de la Ley 681 de 2001, mediante los cuales se "
        "establece la fórmula para determinar los componentes de la estructura de precios del combustible de aviación JET "
        "A-1, se hará efectiva cuando el Gobierno Nacional asigne las funciones a un ente regulador")


def fix_681_116(act):
    """arts. 10, 11 and the parágrafo of art. 12 (the Jet A1 price formula): the page marks them 'derogado por el
    artículo 276 de la Ley 1450 de 2011. En los términos establecidos en el artículo 116 de la misma Ley', and quotes
    art. 116: the repeal 'se hará efectiva cuando el Gobierno Nacional asigne las funciones a un ente regulador ... y se
    dicte la primera regulación sobre el particular'. The source gives no day on which that condition was met (Decreto
    4130 de 2011, quoted under art. 12, reassigned the tariff function to the Comisión de Regulación de Energía y Gas
    with a six-month transition, but no first regulation is dated). As the page reads them, they are out from Ley 1450
    de 2011's day (16 June 2011), credited to it; the condition is recorded here (decision only, no word change)."""
    H.B23._need(all(A116 in H._nv(H.B23._unit(L681, n)) for n in ("10", "11")), "L681 arts. 10/11 art. 116 quote")
    u12 = H.B23._unit(L681, "12")
    H.B23._need(A116 in H._nv(u12) and "Decreto 4130 de 2011" in H._nv(u12), "L681 art. 12 NV")
    h10 = H._hist(act, "art-0010")
    H.B23._need([(d, c) for d, _, c in h10] == [("2001-08-10", None), ("2011-06-16", ["ley-1450-2011"])] and h10[1][1] is None,
                f"L681 art. 10 {H._shape(h10)}")
    H._done(T681, fix_681_116)


H.FIXES[S681] = [fix_681_116]
