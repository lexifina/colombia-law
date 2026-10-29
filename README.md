# Colombia: law history in git

The law of Colombia as a git history: one file per provision, one commit per law or ruling on the day it took effect, and the act or ruling that made each change as the commit's author. `git blame` names the Acto Legislativo or the Constitutional Court ruling behind every paragraph; `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `co/`.

**What is in it now**

| Folder | Act | History |
| --- | --- | --- |
| `constitucion/` | Constitución Política de Colombia (1991) | From promulgation (4 July 1991) to today: every Acto Legislativo that amended it, the 1991 Aclaración of Gaceta Constitucional No. 125, and the Constitutional Court rulings that struck amendments or parts of them |
| `codigo-civil/` | Código Civil (Ley 84 de 1873) | From its sanction (26 May 1873), in the 1873 text the source reproduces, to today |
| `ley-1581-2012/` | Ley 1581 de 2012 (protección de datos personales) | From promulgation (18 October 2012) to today |
| `codigo-penal/` | Código Penal (Ley 599 de 2000) | From its entry into force (24 July 2001, one year after promulgation, art. 476) to today |
| `codigo-general-del-proceso/` | Código General del Proceso (Ley 1564 de 2012) | From promulgation (12 July 2012; art. 627 staggers the start of most articles, see the first commit) to today |
| `codigo-sustantivo-del-trabajo/` | Código Sustantivo del Trabajo | From the official edition (Diario Oficial No. 27.622, 7 June 1951; Decretos 2663 and 3743 de 1950) to today |
| `codigo-de-comercio/` | Código de Comercio (Decreto 410 de 1971) | From its issue (27 March 1971; most of it from 1 January 1972, art. 2038) to today |
| `cpaca/` | Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 1437 de 2011) | From its entry into force (2 July 2012, art. 308) to today |
| `codigo-de-procedimiento-penal/` | Código de Procedimiento Penal (Ley 906 de 2004) | From publication (1 September 2004; by judicial district from 2005, art. 530) to today; one change on `futuro` |
| `codigo-de-la-infancia-y-la-adolescencia/` | Código de la Infancia y la Adolescencia (Ley 1098 de 2006) | From promulgation (8 November 2006; most of it six months later, art. 216) to today |
| `codigo-nacional-de-seguridad-y-convivencia-ciudadana/` | Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016) | From its entry into force (29 January 2017, six months after promulgation, art. 243) to today |
| `sistema-de-seguridad-social-integral/` | Ley 100 de 1993 (Sistema de Seguridad Social Integral) | From publication (23 December 1993, art. 289; pensions from 1 April 1994, art. 151) to today |
| `codigo-general-disciplinario/` | Código General Disciplinario (Ley 1952 de 2019) | From promulgation (28 January 2019; in force only from 29 March 2022, see the first commit) to today |
| `codigo-electoral/` | Código Electoral (Decreto 2241 de 1986) | From publication (1 August 1986, art. 218) to today |
| `estatuto-tributario/` | Estatuto Tributario (Decreto 624 de 1989) | From its entry into force (30 May 1989, two months after publication, the decree's art. 3) to today, including the yearly decrees that updated its absolute values before the UVT |
| `estatuto-general-de-contratacion/` | Estatuto General de Contratación de la Administración Pública (Ley 80 de 1993) | From promulgation (28 October 1993; most of it from 1 January 1994, art. 81) to today |
| `estatuto-del-consumidor/` | Estatuto del Consumidor (Ley 1480 de 2011) | From its entry into force (12 April 2012, six months after promulgation, art. 84) to today |
| `codigo-nacional-de-transito/` | Código Nacional de Tránsito Terrestre (Ley 769 de 2002) | From its entry into force (13 December 2002, three months after promulgation, art. 170) to today |
| `estatuto-organico-del-sistema-financiero/` | Estatuto Orgánico del Sistema Financiero (Decreto 663 de 1993) | From its entry into force (2 May 1993, art. 339) to today |
| `codigo-de-minas/` | Código de Minas (Ley 685 de 2001) | From promulgation (8 September 2001, art. 362) to today, including the reform of Ley 1382 de 2010 until Sentencia C-366 de 2011's deferred effect ended (13 May 2013) |
| `codigo-procesal-del-trabajo-1948/` | Código Procesal del Trabajo y de la Seguridad Social (Decreto-Ley 2158 de 1948) | From its entry into force (29 June 1948, five days after issue, art. 156) to its repeal as a whole by Ley 2452 de 2025 (2 April 2026); the folder is empty from that day |
| `codigo-procesal-del-trabajo/` | Código Procesal del Trabajo y de la Seguridad Social (Ley 2452 de 2025) | From its entry into force (2 April 2026, one year after publication, art. 330) to today |
| `regimen-de-insolvencia/` | Régimen de Insolvencia Empresarial (Ley 1116 de 2006) | From promulgation (27 December 2006; most of it six months later, art. 126) to today |
| `servicios-publicos-domiciliarios/` | Régimen de los Servicios Públicos Domiciliarios (Ley 142 de 1994) | From publication (11 July 1994, art. 189) to today |

Where a code's own vigencia article starts different parts on different days, its first commit is dated from the earliest of them and its note quotes the article. One change has no day in any source: Ley 44 de 1981 (Código de Comercio art. 159) is shown on 31 December 1981, the latest day it can have been sanctioned.

The acts come from separate parts of the same build (`corpus.d/`), each checked against today's text on the source before it reached `main`. Where the source gives no text for a provision in some period (most often the 1989 and 1993 wording of articles of the Estatuto Tributario and the Estatuto Orgánico del Sistema Financiero later rewritten), the file reads "[La fuente no da el texto vigente en esta fecha.]" for that period.

**The Código Penal's penalties after 2005.** Ley 890 de 2004, art. 14, raised every penalty of the Parte Especial by a third in the minimum and a half in the maximum, from 1 January 2005, without rewriting the articles. The source prints each article with the raised figures ("con las penas aumentadas") and keeps the earlier wording; this history follows it, so those changes are commits of Ley 890 de 2004 on 1 January 2005. The figures are the publisher's computation of art. 14, as its own warning says. The per-act `README.md` in each folder lists every provision, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 15 say on 1 January 2004 (under Acto Legislativo 2 de 2003)? | `python tools/en_vigor_el.py 2004-01-01 constitucion 15` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2004-01-01T23:59:59Z" main -- constitucion/art-015.md):constitucion/art-015.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2004-01-01T23:59:59Z" main -- constitucion/art-015.md; git show "$($r):constitucion/art-015.md"` |
| Which act or ruling wrote each paragraph of art. 221? | `git blame constitucion/art-221.md` |
| Every change to art. 34, word by word | `git log -p --word-diff constitucion/art-034.md` |
| Every act and ruling in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one act changed | `git show law/al-2-2015` (tags `law/<key>` mark each law's commit) |
| What the Court struck | `git log --author="Sentencia" --format="%ad %an %s" --date=short` |
| The whole Constitution on a date | `python tools/en_vigor_el.py 2000-01-01 constitucion` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Source

The text and every date come from the **Secretaría General del Senado**'s "basedoc" collection ([secretariasenado.gov.co/senado/basedoc](http://www.secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991.html)), compiled by Avance Jurídico and updated to 15 October 2026 (Diario Oficial No. 53.651). It is the only free official site that keeps, for each provision, the earlier texts ("Legislación Anterior": "Texto original de la Constitución Política", "Texto modificado por el Acto Legislativo 2 de 2003"), notes naming the act that changed it with its Diario Oficial date ("Notas de Vigencia"), and the Constitutional Court rulings on it ("Jurisprudencia Vigencia").

The source has **no dated snapshots**. Each version here is rebuilt from those earlier texts and from the source's inline amendment markers ("<Inciso adicionado por el artículo 1 del Acto Legislativo 1 de 2005 ...>"). Today's text in the repository was checked against the source's current text, provision by provision, on 28 October 2026: all 496 provisions match (`tools/verify.py`).

## Dates

- Each commit is dated at **noon, America/Bogota, on the day the change took effect**. Enactment and publication dates are trailers (`Enacted:`, `Published:`); the in-force day is in `In-force:`, which the tools read.
- **Actos Legislativos** take effect on the day of their publication in the Diario Oficial, as the source's notes say ("Rige a partir de su publicación"), unless the note quotes another vigencia clause: Acto Legislativo 1 de 2001 from 1 January 2002; Actos Legislativos 1 and 4 de 2007 from 1 January 2008; and the clauses tied to elections, Acto Legislativo 2 de 2005 (12 March 2006), 3 de 2005 (14 March 2010) and 3 de 2007 (28 October 2007). The election days come from the Registraduría Nacional del Estado Civil, read from cached pages by `tools/parse.py`: its [Calendario Electoral 2006 - 2010](https://www.registraduria.gov.co/Calendario-Electoral-2006-2010.html) (Resolución 0497 de 2005), its [Comunicado de Prensa No. 050 de 2009](https://web.archive.org/web/20110726040247id_/http://www.registraduria.gov.co/ESTA-LISTO-EL-PRE-CALENDARIO.html) (Internet Archive copy), and its [home page of 30 September 2007](https://web.archive.org/web/20070930160642id_/http://www.registraduria.gov.co/) ("el proceso electoral del 28 de octubre"; the year is the capture's). Each of those commits names its source in the message.
- **Default rule** for ordinary laws: Ley 4 de 1913 (Código de Régimen Político y Municipal), arts. 52 and 53: a law binds two months after promulgation unless it fixes its own date.
- **The Constitution of 1991** took effect on its promulgation (art. 380), in Gaceta Constitucional No. 114 of 4 July 1991. The source gives the text of the second corrected edition (Gaceta No. 116 of 20 July 1991), which is the first commit; the corrections of the Aclaración published in Gaceta No. 125 (25 September 1991) are a commit of their own.
- **Court rulings** (Corte Constitucional) are dated by the day of the ruling, as the source gives it.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a change that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## What "author" means

The author of a commit is the act or ruling that made the change, with an e-mail address that cannot exist (`al-2-2015@secretariasenado.invalid`), so `git blame` and `git log --author` name them. The committer is always Lexifina.

- **Credits come only from the source.** A change is credited to an Acto Legislativo only when the source's earlier texts, markers or notes name it.
- **Constitutional Court rulings are authors too** (kind `court`). When the Court struck a whole Acto Legislativo (for example Sentencia C-816 de 2004 on Acto Legislativo 2 de 2003, C-740 de 2013 on Acto Legislativo 2 de 2012, C-294 de 2021 on Acto Legislativo 1 de 2020), the provision returns, on the ruling's day, to its text before that act. When it struck words ("<Aparte tachado INEXEQUIBLE>"), the struck words are in the text until the ruling and gone after it.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each act changed.

## What it does not show

- **Gaps in the source.** For a few provisions the source names an act that changed them but gives no text for the period after it (a later act rewrote the same words, and only the latest text is kept). There the file reads `[La fuente no da el texto vigente en esta fecha.]` for that period, credited to the act named; nothing is guessed. The cases (arts. 122, 256, 263, 322, 328 and 361) are listed in `REPRODUCE.md`. Art. 263 also holds the text of the former art. 263-A, which Acto Legislativo 2 de 2015 moved there.
- **Rulings that change no words.** Plain EXEQUIBLE rulings, inhibitions and "estarse a lo resuelto" rulings are not recorded.
- **Avance Jurídico's editorial notes**, concordances and commentary are not in the text; the notes are used only to date and credit changes.
- **The first printing** of the Constitution (Gaceta No. 114) is not in the source; the history starts with the corrected text of Gaceta No. 116.

## How it is built

`tools/fetch.py` downloads every page once through curl (one request per second, cached by the sha256 of the URL), `tools/parse.py` turns the cache into `corpus.json`, and the shared builder `tools/build.py` writes the history with `git fast-import`. The same corpus always gives the same hashes. `REPRODUCE.md` records every command, tool version, data hash and decision, and the result of a hash-for-hash rebuild.

No AI model wrote or changed legal text. Claude Opus 5.5 wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Kind | Past versions | Names the amending act | Bulk | Notes |
| --- | --- | --- | --- | --- | --- |
| [Secretaría General del Senado, basedoc](http://www.secretariasenado.gov.co/senado/basedoc/) | Official legislation (compiled by Avance Jurídico) | earlier texts per provision, no dated snapshots | yes, per provision, with Diario Oficial dates and Court rulings | per document (HTML pages plus one JavaScript file per page holding the note boxes) | Used |
| [SUIN-Juriscol](https://www.suin-juriscol.gov.co) (Ministerio de Justicia) | Official legislation | no dated versions seen | yes ("Adicionado por: Art. 2 Ley 1482 de 2011"), with Court rulings attached | no | An Angular app that serves no text to a plain request; it does not keep earlier texts. Not used |
| [Registraduría Nacional del Estado Civil](https://www.registraduria.gov.co) | Electoral authority | n/a | n/a | no | Used only for the days of three elections that Actos Legislativos take effect on (two pages through Internet Archive captures pinned by timestamp) |
| Diario Oficial (Imprenta Nacional) | Official gazette | n/a | n/a | no | Not read; the source gives the Diario Oficial number and date of every act |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

The Constitution, laws and judicial decisions of Colombia may be reproduced freely (Ley 23 de 1982, art. 41), provided the official text is reproduced faithfully. Fuente: Secretaría General del Senado de la República, www.secretariasenado.gov.co. The arrangement, tables, commit messages and tools are by Lexifina, under the terms in `LICENSE`.

This repository is not legal advice and not an official publication.

## En español

Historia del derecho colombiano en git: un archivo por disposición y un commit por acto o sentencia, fechado el día de su entrada en vigencia y firmado por el acto legislativo o la sentencia de la Corte Constitucional que hizo el cambio (`git blame` nombra la norma de cada párrafo). Contiene la Constitución Política de 1991 desde su promulgación el 4 de julio de 1991, con todos sus Actos Legislativos y las sentencias que los declararon inexequibles, y los códigos y leyes de la tabla de arriba (entre ellos el Código Civil, el Código Penal, el Código General del Proceso, el CPACA, el Estatuto Tributario, la Ley 80 de 1993, el Estatuto del Consumidor, el Código Nacional de Tránsito, el Estatuto Orgánico del Sistema Financiero, el Código de Minas, los dos Códigos Procesales del Trabajo (Decreto-Ley 2158 de 1948, derogado desde el 2 de abril de 2026, y Ley 2452 de 2025), la Ley 1116 de 2006 y la Ley 142 de 1994).

- Texto vigente en una fecha: `python tools/en_vigor_el.py 2004-01-01 constitucion 15`
- Fuente: Secretaría General del Senado (basedoc). La fuente no tiene versiones fechadas: cada versión se reconstruye con la "Legislación Anterior", las notas de vigencia y las marcas de modificación de la propia fuente. El texto de hoy coincide con el de la fuente en las 496 disposiciones (28 de octubre de 2026).
- Fechas: los Actos Legislativos rigen desde su publicación en el Diario Oficial, salvo que la nota cite otra regla de vigencia; las sentencias, desde su fecha. Regla supletoria para las leyes: Ley 4 de 1913, arts. 52 y 53.
- Donde la fuente no da el texto de un período, el archivo dice "[La fuente no da el texto vigente en esta fecha.]". Ningún modelo de IA escribió texto legal.
