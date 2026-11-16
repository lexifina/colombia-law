# Tools

The scripts behind this Colombia-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/colombia-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only colombia-law, its commit and its
language (`es`). `build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py` and `patch_co.py` sit two
folders above the scripts, next to `config.json`.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps paths to the folders since the move (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change |
| `map_moved.py` | Rewrites the paths in the history table to each act's folder since the move of 10 November 2026 (`data/paths.json`), so that an act's history is not split in two at the move; `run.sh` runs it after the history is indexed |
| `patch_co.py` | The Colombian date forms below, in the copy of global-law's scripts (`python -X utf8 patch_co.py <scripts dir>`; a fix already in place is skipped) |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (here all 4, 1 of them with the old and the new date in one sentence) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Spanish and English, light and dark |
| `config.json` | The repository, the Spanish category names, the files that are not law, and the chart's labels |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`; a fix already in place is skipped) |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py` | The same for Vietnamese, Spanish (Spain), Catalan, English and German forms, found by the runs on those repositories; already applied to the copy used here. Of them, `patch_es.py`'s date forms ("hasta el día 30 de junio", "31 de diciembre del (año) 2020") also serve Colombian Spanish |
| `redo.py` | Runs `patch_detectors.py`, `patch_detectors_vi.py` and `patch_es.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--full` runs every step again through `run.sh` and keeps every review already made; `EMBED_FONTS` names the script that embeds the chart's fonts). It does not run `patch_co.py`; run it first |
| `basedoc_note.py` | Hand-check helper: for one article of a page of the Senate's basedoc (and the page's script, which holds its notes), the text and the notes that name a ruling or give the earlier text, with struck-out words in `[[ ]]` (`python -X utf8 basedoc_note.py <dir> <page stem> <article> <ruling>`) |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(data/|tools/|README|REPRODUCE|LICENSE|jurisdiction\.json)|/README\.md$'`; every act
is in a folder of acts, so the review of lapsed time limits in law texts drew the same 40 flags as the review of all of them.

The detectors in this copy already carry every fix of the patch scripts above. Changes made for this repository:

- `add_root.py` counts as law, besides laws and amendments, the `Kind:` values this repository gives decrees (`decree`), the
  oldest available text of an act (`publisher`) and Constitutional Court rulings that struck out text (`court`): 4,936 of
  the 4,955 commits; of the other 19, 2 are documentation (`Kind: documentation`) and 17 carry no `In-force:` trailer.
  Without `court`, an article the Court struck out would look, to the history detectors, as if it had never been removed.
- `patch_co.py`, Colombian dates: the time-limit search now also reads the day as an ordinal ("1o de enero", "1o. de
  julio", "1º de enero"), the day or the year in words with the figure in brackets ("hasta el treinta y uno (31) de
  diciembre de dos mil cinco (2005)", "hasta el primero (1o) de abril de 2017"), and deadlines "a más tardar el 31 de
  diciembre de 2020", as it reads "no later than" in English. Lapsed time limits went from 311 to 533 (154 of them
  deadlines), empty periods from 2 to 4; the empty-period search leaves deadlines out, as before. The first run was made
  without it; `ingest/textscan.py`, `detectors/text_detectors.py` and `detectors/late_extension.py` were then run again
  (after deleting `index/dates`, `index/amounts`, `index/amount_changes` and their findings), before the model review.
- `config.json` gives the chart a shorter Spanish label for references to deleted provisions ("Remisiones a artículos
  inexistentes"), which otherwise ran into its bar.
