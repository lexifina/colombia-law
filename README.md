# Colombia: law history in git


The national law of Colombia as a git history: one file per article, one commit per law or ruling on the day it took effect, and the act or ruling that made each change as the commit's author. `git blame` names the law or ruling behind every paragraph; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Colombia's national law, which global-law reads at `colombia/national/acts/`.

**What is in it now:** 2,392 acts with 6,166 versions from 1873 on: the Constitution of 1991, with the 63 Actos Legislativos and the court rulings that changed it, and 2,354 laws and 37 decrees, among them 34 codes. 1,958 of the acts start from the oldest text the source publishes, not from their enactment; 18 have since been repealed, and their history ends with a version that has no provisions; 9 versions, due to take effect after 2 November 2026, are on the `futuro` branch. [`data/versions.json`](data/versions.json) lists every act with the day each version took effect; [`data/laws.csv`](data/laws.csv) lists the 2,692 laws, decrees and rulings behind the changes, with their dates.

Each act is a folder, mostly `<kind>/<year>/<number>/` (`ley/2002/789/` is Ley 789 de 2002); the Constitution is `constitution/constitucion/` and 25 codes are in `code/` (`code/codigo-sustantivo-del-trabajo/` is the Código Sustantivo del Trabajo). Each article is one file (`art-0161.md`), the headings of books, titles and chapters are in `titulos.md`, and 197 acts are one file, `texto.md`. [`data/paths.json`](data/paths.json) maps each act id to its folder.

The text is in Spanish, as the Senate's basedoc prints it, without the editorial notes and concordances of Avance Jurídico, which prepares that compilation. An English translation is not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to art. 161 of the Código Sustantivo del Trabajo | `git log -p --word-diff --follow -- code/codigo-sustantivo-del-trabajo/art-0161.md` |
| Which law wrote each line of art. 161? | `git blame code/codigo-sustantivo-del-trabajo/art-0161.md` |
| Every version of the Código Sustantivo del Trabajo, with the day each took effect | `git log --diff-filter=r --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- code/codigo-sustantivo-del-trabajo codigo-sustantivo-del-trabajo ":^*/README.md"` |
| Art. 161 as in force on 1 January 2020 | `python tools/on.py 2020-01-01 code/codigo-sustantivo-del-trabajo art-0161` |

On 2026-11-10 the acts moved to their present folders: `--follow` and the old folder name (`codigo-sustantivo-del-trabajo`) reach the history before the move, and `--diff-filter=r` leaves the move itself out.

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Colombian law](https://global-law.lexifina.com/v1/try_claude?country=colombia)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=colombia)**: the same question in ChatGPT.
- **[Search Colombian law on our site](https://lexifina.com/law?country=colombia&q=vacaciones+anuales)**: a search for "vacaciones anuales", with each provision's text and its versions, no account needed.
- **[Developer REST API](https://global-law.lexifina.com/v1/search_law?query=vacaciones+anuales&jurisdiction=colombia)**: the same search as JSON, with no key. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Spanish or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add colombia/national/acts
python3 tools/law.py show 2026-01-01 colombia/national/acts/code/codigo-sustantivo-del-trabajo/art-0161.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, America/Bogota, on the day the change took effect, and carries it in its `In-force:` trailer, beside `Enacted:` and `Published:`:

- a law's own vigencia clause decides; without one, Ley 4 de 1913 (Código de Régimen Político y Municipal), arts. 52 and 53, puts it two months after promulgation. Actos Legislativos take effect on publication in the Diario Oficial unless they fix another day (three of them an election day, taken from the Registraduría);
- a ruling that strikes text takes effect on the day of the ruling, unless the Court says otherwise (Ley 270 de 1996, art. 45);
- an act that starts from its oldest available text starts on the latest day the source's notes give for that text or, without such notes, on the act's own start;
- git cannot store dates before 1970, so the 47 earlier commits are dated from 1970-01-01, one second apart, with the real day in `In-force:`. Ask for a date with `tools/on.py`, not `git log --before`.

Each change is credited to the law, decree, Acto Legislativo or ruling that made it, with an address that cannot exist (`Ley 2466 de 2025 <ley-2466-2025@secretariasenado.invalid>`, `Sentencia C-081 de 2026`), so `git blame` and `git log --author` name laws and rulings. An act's oldest available text is credited to the publisher, `Secretaría General del Senado (basedoc)`, as the "oldest version available"; the committer is Lexifina.

## How it is checked

- `tools/check_repo.py` reads every version back from git on the day it took effect and on the day before, and compares it, file by file, with the corpus whose sha256 is in `data/corpus.sha256`; it also checks that every commit's trailers parse, that `main` has no merge commits and that nothing is dated in the future.
- `tools/verify.py` compares each act's latest version in the corpus with today's text on the basedoc page, editorial markers and struck words removed.
- The same corpus gives the same commit hashes (`tools/build.py`). [`REPRODUCE.md`](REPRODUCE.md) records no result of these checks for the present build yet, and no second build compared.
- History is append-only (`tools/append.py`): new acts and later versions go on top, and no published commit is rewritten.

## What it does not show

- **Most decrees and older law.** Only 37 decrees (17 of them codes and estatutos) and, besides the Constitution, 18 acts from before 1992 are here; regulatory decrees, resolutions and departmental and municipal law are not.
- **Changes before an act's oldest available text.** For 1,958 acts the source gives no earlier text, so their earlier changes are inside that first commit.
- **Case law**, except the rulings that changed a text: 1,400 of the Constitutional Court, and some of the Supreme Court and the Consejo de Estado, are commits; the rulings themselves are not here.
- **Changes that leave the words alone.** 481 commits change no words (`Words-changed: no`), most of them rulings that upheld a text on a condition; they touch no file, so a log of a path does not list them.
- **Some earlier texts.** Where the source names the act that changed a provision but prints no text after it, the provision reads `[La fuente no da el texto vigente en esta fecha.]` for that period (5 provisions today).

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Secretaría General del Senado, basedoc](http://www.secretariasenado.gov.co/senado/basedoc/) | Official compilation of the Constitution, codes and laws, prepared by Avance Jurídico | yes, for many provisions: their earlier texts and a note on each change | The text of every act; its notes name the act or ruling behind each change, with Diario Oficial numbers and dates |
| [Colpensiones, Normativa](https://normativa.colpensiones.gov.co/colpens/) | Compilation of older acts | n/a | Headings and vigencia clauses of acts before 1992 that the basedoc lacks |
| [Régimen Legal de Bogotá](https://www.alcaldiabogota.gov.co/sisjur/), [DIAN, Compilación Jurídica](https://normograma.dian.gov.co/) | Official compilations | n/a | The in-force day of three decrees the basedoc lacks |
| Registraduría Nacional del Estado Civil | Electoral authority | n/a | The days of three elections on which Actos Legislativos took effect |

## Licence

See [`LICENSE`](LICENSE). Under Ley 23 de 1982, art. 41, the Constitution, laws, decrees and judicial decisions may be reproduced freely, provided the official text is reproduced faithfully; Avance Jurídico's notes, concordances and commentary are not reproduced, only the official text and the facts its notes state. Lexifina's own contributions (the arrangement, commit messages, tables and tools) are CC0 1.0.

No AI model wrote, translated or corrected legal text, and none runs at build time; the scripts were written by Claude Code running Claude Opus 5.5 (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
