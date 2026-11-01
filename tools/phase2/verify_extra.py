"""Extra readings for the batch checks (verify_batchN.py): articles not in force today although the page still prints
words under them.

- '<Artículo derogado por el artículo N de la Ley X>' followed by the article's last words (no date in the marker): the
  act repealed the whole article, which is gone today.
- '<Artículo INEXEQUIBLE>' followed by words, with the ruling note 'Artículo declarado INEXEQUIBLE': struck whole.
"""
import re

REPEALED = re.compile(r'^\s*(?:<span class="b_aj">)?&lt;Art&iacute;culo derogado por el art&iacute;culo <A [^>]*>\d+</A> '
                      r'de la (?:Ley|Decreto) \d+ de \d{4}&gt;')
STRUCK = re.compile(r'^\s*(?:<span class="b_aj">)?&lt;Art&iacute;culo INEXEQUIBLE&gt;')


def install(V) -> None:
    today = V.today

    def today_gone(name):
        out = today(name)
        for u in V.P.doc_units(name)[1:]:
            ps = [it for it in u["items"] if it[0] == "p"]
            num = V.E.label_num(u["label"] or "")
            if not ps or not num:
                continue
            la = any(it[0] == "box" and it[1] == "Legislación Anterior" for it in u["items"])
            jv = " ".join(V.E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")
            if (REPEALED.match(ps[0][1]) and not la) or (STRUCK.match(ps[0][1]) and "Artículo declarado INEXEQUIBLE" in jv):
                out[V.E.unit_key(num)[0]] = []
        return out

    V.today = today_gone
