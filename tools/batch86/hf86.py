"""Hand-set histories for batch 86 (Leyes 98 de 1993, 1473 de 2011, 232 de 1995), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L1473, T1473 = "ley_1473_2011", "Regla fiscal (Ley 1473 de 2011)"

# art. 11 ('Excepciones'): the page prints its words under '<Artículo derogado a partir del 1 de enero de 2022 por el
# artículo 65 de la Ley 2155 de 2021>' (no earlier-text box): the words stand from the act's first day (1 January 2012)
# and leave on 1 January 2022, credited to Ley 2155 de 2021 (the engine had the placeholder until Ley 2155's promulgation).
H.PRINTED[L1473] = [("Artículo derogado a partir del 1 de enero de 2022 por el artículo 65 de la Ley 2155 de 2021",
                     "ley-2155-2021", "2022-01-01")]
H.FIXES["regla-fiscal-2011"] = [H.fix_printed(L1473, T1473)]
