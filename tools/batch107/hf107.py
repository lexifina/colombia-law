"""Hand-set histories for batch 107 (Ley 179 de 1994), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import html as _html
import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L179, S179 = "ley_0179_1994", "reforma-del-presupuesto-1994"
T179 = "Reforma de la Ley Orgánica de Presupuesto (Ley 179 de 1994)"
SEN = "http://www.secretariasenado.gov.co/senado/basedoc/"


def _ruling_text(href):
    """Plain text of a cached ruling page (the Senado basedoc copy)."""
    raw = H.E.read(SEN + href)
    H.B23._need(raw is not None, f"{href} not cached")
    raw = raw.encode("latin-1").decode("utf-8", "replace")
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", raw)))


def _hist_check(act, key, days):
    h = H._hist(act, key)
    H.B23._need([d for d, _, _ in h] == days, f"L179 {key} shape {H._shape(h)}")
    return h


# Ley 225 de 1995 art. 2's text of art. 12 (the page's 'Texto modificado por la Ley 225 de 1995' box), as the verifier
# reads it: today's text is this one, while the page prints Ley 1687 de 2013's under its deferred-strike marker.
def text_225_12():
    u = H.B23._unit(L179, "12")
    return H.B23._box_lines(H.B23._boxes(u, "Legislación Anterior")[0], "Texto modificado por la Ley 225 de 1995", True)


def fix_12(act):
    """Ley 179 de 1994, art. 12 (contribuciones parafiscales). Ley 1687 de 2013 art. 81 (the 2014 budget act, in force
    on its publication, 11 December 2013, art. 112) rewrote it; Sentencia C-052-15 (12 February 2015) declared that
    article INEXEQUIBLE with its effects deferred to 31 December 2015 (the page's marker '<Artículo INEXEQUIBLE, con los
    efectos diferidos hasta el 31 de diciembre de 2015>'). The engine had the placeholder from 2013 and the article out
    from the ruling's day. Now Ley 1687's words (the page's text) stand from 11 December 2013 and leave on 31 December
    2015 (the deferral's day, as for every deferred strike in the corpus), credited to the ruling, when the text Ley 225
    de 1995 art. 2 had given the article (the page's 'Texto modificado por la Ley 225 de 1995' box) is in force again:
    the strike of the amending article takes its amendment out, and the Estatuto Orgánico del Presupuesto's page
    (Decreto 111 de 1996 art. 29, which compiles this article) prints that text as today's."""
    E = H.E
    u = H.B23._unit(L179, "12")
    H.B23._need("Artículo 81 de la Ley 1687 de 2013 declarado INEXEQUIBLE, con los efectos diferidos hasta el 31 de "
                "diciembre de 2015, por la Corte Constitucional mediante Sentencia C-052-15 de 12 de febrero de 2015"
                in H._jv(u) and "Rige a partir del 1o. de enero de 2014 (Art. 112)" in H._nv(u), "L179 art. 12 page")
    l225 = text_225_12()
    h = _hist_check(act, "art-0012", ["1994-12-30", "1995-12-20", "2013-12-11", "2015-02-12"])
    H.B23._need(h[1][1] == l225 and h[2][1] == [H.PH] and h[3][1] is None, "L179 art. 12 texts")
    c052 = E.add_court("C-052-15", "2015-02-12", "c-052_2015.html")
    H._set(act, "art-0012", H._label(act, "art-0012"),
           [(None, h[0][1], None), ("1995-12-20", l225, "ley-225-1995"), ("2013-12-11", H._printed(u), "ley-1687-2013"),
            ("2015-12-31", l225, c052)])
    H.B23._forget(L179, "art-0012")
    H._done(T179, fix_12)


def fix_21(act):
    """Ley 179 de 1994, art. 21 (excedentes financieros). The page prints the second inciso as Ley 225 de 1995 art. 21
    left it: the phrase that act put at its start ('"De los excedentes financieros ... En los demás casos"', in force 20
    December 1995), then the original words 'El Gobierno hará ... excedente financiero de la Nación', shown struck by
    Sentencia C-023-96 (23 January 1996; the Court 'no tuvo en cuenta la adición'). The engine had the original inciso
    in no version and the placeholder from Ley 225's day. Now: from the act's first day the original inciso (the struck
    words); from 20 December 1995 the phrase in front of them; from 23 January 1996 the phrase alone."""
    u = H.B23._unit(L179, "21")
    H.B23._need("Aparte tachado original declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-023-96, "
                "del 23 de enero de 1996" in H._jv(u) and "Inciso adicionado por artículo 21 de la la Ley 225 de 1995"
                in H._nv(u), "L179 art. 21 page")
    h = _hist_check(act, "art-0021", ["1994-12-30", "1995-12-20", "1996-01-23"])
    full, now = H._printed(u, True), H._printed(u)
    H.B23._need(h[2][1] == now and len(full) == len(now) == 3 and full[:2] == now[:2] and h[0][1] == now[:2],
                "L179 art. 21 texts")
    m = re.match(r'("De los excedentes financieros, .*En los demás casos") (El Gobierno hará .*)$', full[2])
    H.B23._need(m and now[2] == m.group(1) + ".", "L179 art. 21 inciso 2")
    H._set(act, "art-0021", H._label(act, "art-0021"),
           [(None, now[:2] + [m.group(2)], None), ("1995-12-20", full, "ley-225-1995"), ("1996-01-23", now, h[2][2][0])])
    H.B23._forget(L179, "art-0021")
    H._done(T179, fix_21)


def fix_26_27(act):
    """Ley 179 de 1994, arts. 26 (inciso 3o.) and 27: the word 'Cuartas' (the budget committees), which the page shows
    struck by Sentencia C-353-95. The page's box names the ruling but gives no day, so the engine had left the word out
    of every version. The ruling's own text (the Senado's copy) is dated 9 August 1995 ('Sentencia aprobada en Santa Fe
    de Bogotá, D.C., según consta en acta del nueve (9) de agosto de mil novecientos noventa y cinco (1995)') and
    declares INEXEQUIBLE 'las expresiones "cuartas", contenidas en los artículos 26, inciso 3º, y 27 de la Ley 179 de
    1994': the word stands from the act's first day and leaves on 9 August 1995, credited to the ruling."""
    E = H.E
    t = _ruling_text("c-353_1995.html")
    H.B23._need("según consta en acta del nueve (9) de agosto de mil novecientos noventa y cinco (1995)" in t and
                'Decláranse INEXEQUIBLES las expresiones "cuartas", contenidas en los artículos 26, inciso 3º, y 27 de la '
                'Ley 179 de 1994' in t, "C-353-95 ruling text")
    c = E.add_court("C-353-95", "1995-08-09", "c-353_1995.html")
    E.LAWS[c]["note"] = None
    for num in ("26", "27"):
        key = E.unit_key(num)[0]
        u = H.B23._unit(L179, num)
        H.B23._need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-353-95"
                    in H._jv(u), f"L179 art. {num} page")
        before, after = H._printed(u, True), H._printed(u)
        H.B23._need(len(before) == len(after) and sum(b != a for b, a in zip(before, after)) == 1
                    and sum(b.count("Cuartas") - a.count("Cuartas") for b, a in zip(before, after)) == 1,
                    f"L179 {num} struck")
        h = _hist_check(act, key, ["1994-12-30"])
        H.B23._need(h[0][1] == after, f"L179 {key} text")
        H._set(act, key, H._label(act, key), [(None, before, None), ("1995-08-09", after, c)])
        H.B23._forget(L179, key)
    H._done(T179, fix_26_27)


def fix_38(act):
    """Ley 179 de 1994, art. 38 (art. 72 of Ley 38 de 1989: apropiaciones, reservas). The page prints the text Ley 225
    de 1995 art. 8 gave it (in force 20 December 1995) and the act's own text in its 'Texto original de la Ley 179 de
    1994' box; the engine had today's text from 1994. Now the box's text from the act's first day, Ley 225's from 20
    December 1995."""
    u = H.B23._unit(L179, "38")
    H.B23._need("fue modificado por artículo 8 de la la Ley 225 de 1995, publicada en el Diario Oficial No. 42.157 del "
                "20 de diciembre de 1995" in H._nv(u), "L179 art. 38 page")
    orig = H.B23._box_lines(H.B23._boxes(u, "Legislación Anterior")[0], "Texto original de la Ley 179 de 1994", True)
    h = _hist_check(act, "art-0038", ["1994-12-30"])
    H.B23._need(h[0][1] == H._printed(u) and len(orig) == 4, "L179 art. 38 texts")
    H._set(act, "art-0038", H._label(act, "art-0038"),
           [(None, orig, None), ("1995-12-20", h[0][1], H.E.register("ley-225-1995"))])
    H.B23._forget(L179, "art-0038")
    H._done(T179, fix_38)


def fix_55(act):
    """Ley 179 de 1994, art. 55 (list of changes to Ley 38 de 1989). The page prints, in the place of the act's
    incisos 9 and 12, the texts Ley 225 de 1995 arts. 5 and 6 gave the provisions of Ley 38 those incisos had changed
    (in force 20 December 1995), and the incisos as enacted in 'Texto original' boxes; the engine had Ley 225's words
    from 1994. Now the two original incisos stand from the act's first day and give way to Ley 225's words on 20 December
    1995 (the day inciso 18 goes, repealed by its art. 33, as the engine has it)."""
    u = H.B23._unit(L179, "55")
    nv = H._nv(u)
    H.B23._need("modificado por el inciso 9 del texto original de la Ley 179 de 1994 fue modificado por artículo 5 de la "
                "la Ley 225 de 1995" in nv and "modificado por el inciso 12 del texto original de la Ley 179 de 1994 fue "
                "modificado por artículo 6 de la Ley 225 de 1995" in nv, "L179 art. 55 page")
    boxes = [H.B23._box_lines(b, "Texto original de la Ley 179 de 1994", True)
             for b in H.B23._boxes(u, "Legislación Anterior")]
    H.B23._need([len(b) for b in boxes] == [1, 1, 1]
                and boxes[0][0].startswith("Sustituir en el parágrafo 1o., del artículo 12")
                and boxes[1][0].startswith("Eliminar la expresión 'en el Plan Operativo Anual de Inversión'"),
                "L179 art. 55 boxes")
    h = _hist_check(act, "art-0055", ["1994-12-30", "1995-12-20"])
    v1, v2 = h[0][1], h[1][1]
    i9 = next(i for i, x in enumerate(v1)
              if x.startswith("El inciso primero y el parágrafo primero del artículo 12 de la Ley 38"))
    i12 = next(i for i, x in enumerate(v1)
               if x.startswith("Los excedentes financieros de las empresas industriales y comerciales"))
    H.B23._need(v1[i9 + 1].startswith("Unidad de Caja:") and v1[i9 + 2].startswith("PARÁGRAFO 1o.") and i12 == i9 + 5
                and v1[i12 + 3].startswith("El Consejo Nacional de Política Económica y Social, Conpes, al adoptar")
                and [x for x in v1 if x not in v2] == [boxes[2][0]], "L179 art. 55 lines")
    orig = v1[:i9] + boxes[0] + v1[i9 + 3:i12] + boxes[1] + v1[i12 + 4:]
    H._set(act, "art-0055", H._label(act, "art-0055"), [(None, orig, None), ("1995-12-20", v2, h[1][2][0])])
    H.B23._forget(L179, "art-0055")
    H._done(T179, fix_55)


def fix_63_c220(act):
    """Ley 179 de 1994, art. 63: Sentencia C-220-97 upheld it on a condition (as art. 4 of Decreto 111 de 1996, which
    compiles it); this page's box dates the ruling '29 de mayo 1997' and the Estatuto Orgánico del Presupuesto's page
    '29 de abril de 1999'. The ruling's own text (the Senado's copy) is dated 'abril veintinueve (29) de mil novecientos
    noventa y siete (1997)': the note's version is on 29 April 1997, the day the other part holding the ruling
    (fix_law_entries.py) gives it too."""
    E = H.E
    t = _ruling_text("c-220_1997.html")
    H.B23._need("abril veintinueve (29) de mil novecientos noventa y siete (1997)" in t and
                "cuyo texto corresponde al artículo 63 de la ley 179 de 1994" in t, "C-220-97 ruling text")
    k = "c-220-97"
    H.B23._need(E.LAWS[k]["enacted"] == "1997-05-29", f"c-220-97 {E.LAWS[k]['enacted']}")
    vs = act["versions"]
    i = next(i for i, v in enumerate(vs) if v["from"] == "1997-05-29")
    H.B23._need(vs[i]["credits"] == {"art-0063": [k]} and vs[i - 1]["from"] < "1997-04-29", "c-220-97 version")
    vs[i]["from"] = "1997-04-29"
    E.LAWS[k]["enacted"] = "1997-04-29"
    H._done(T179, fix_63_c220)


def fix_70(act):
    """Ley 179 de 1994, art. 70 (enajenación de participaciones estatales). Sentencia C-596-95 (7 December 1995) struck
    its incisos 1o. to 3o.; the page prints only the fourth, and the three in its 'Texto ariginal Ley 179 de 1994' box
    (the publisher's '<INCISO n>' labels left out). The engine had the fourth inciso alone from 1994. Now the four from
    the act's first day, the fourth alone from the ruling's day, credited to it."""
    E = H.E
    u = H.B23._unit(L179, "70")
    H.B23._need("Incisos 1o., 2o., y 3o. declarados INEXEQUIBLES por la Corte Constitucional mediante Sentencia C-596-95, "
                "del 7 de diciembre de 1995" in H._jv(u), "L179 art. 70 page")
    box = H.B23._box_lines(H.B23._boxes(u, "Legislación Anterior")[0], "Texto ariginal Ley 179 de 1994", True)
    h = _hist_check(act, "art-0070", ["1994-12-30"])
    now = h[0][1]
    H.B23._need(len(box) == 3 and now[0] == "NUEVO." and len(now) == 2 and now[1].startswith("En cualquier evento"),
                "L179 art. 70 texts")
    c = E.add_court("C-596-95", "1995-12-07", "c-596_1995.html")
    E.LAWS[c]["note"] = None
    orig = now[:1] + box + now[1:]
    H._set(act, "art-0070", H._label(act, "art-0070"), [(None, orig, None), ("1995-12-07", now, c)])
    H.B23._forget(L179, "art-0070")
    H._done(T179, fix_70)


def note_67(act):
    """Ley 179 de 1994, art. 67 (rentas contractuales): the page heads it '<Este artículo no se encuentra vigente, ni
    está produciento efectos jurídicos. Ver Jurisprudencia Vigencia>'; the box quotes the reasoning of Sentencia C-066-03
    (and C-208-03), in which the Court declared itself INHIBIDA: no act or ruling the source names took the article out
    on a day. Its words stand in every version."""
    u = H.B23._unit(L179, "67")
    H.B23._need("los cuales no se encuentran vigentes y no están produciendo efectos" in H._jv(u)
                and "se declaró INHIBIDA" in H._jv(u), "L179 art. 67 page")
    _hist_check(act, "art-0067", ["1994-12-30"])
    H._done(T179, note_67)


def note_71(act):
    """Ley 179 de 1994, art. 71 (vigencia): 'La presente Ley rige a partir de su vigencia excepto lo referente a la
    ejecución y seguimiento presupuestal que empieza a regir el 1o. de enero de 1995'. The act is dated from its
    publication (Diario Oficial No. 41.659 of 30 December 1994); the clause names no article for the execution
    exception, which starts two days later, so no article is dated apart."""
    u = H.B23._unit(L179, "71")
    H.B23._need("excepto lo referente a la ejecuci" in " ".join(H._printed(u)) and act["versions"][0]["from"] == "1994-12-30",
                "L179 art. 71")
    H._done(T179, note_71)


H.FIXES[S179] = [fix_12, fix_21, fix_26_27, fix_38, fix_55, fix_63_c220, fix_70, note_67, note_71]
