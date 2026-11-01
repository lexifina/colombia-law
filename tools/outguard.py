"""Where a parser writes its part (2026-11-01, tenth session).

Default: the driver's own folder's .tmp (batchN/.tmp for batchN/parse_batchN.py). A part lands in corpus.d (or the
Constitution's corpus.json) only when the command line carries --install or --write, so no part can reach the installed
corpus before its checks. --out-dir DIR / --out FILE still choose any other place; pointing them at corpus.d needs the
flag too. Every writer calls guard(path) just before it writes, which stops the run otherwise.
"""
from __future__ import annotations

import os
import sys

COUNTRY = os.path.dirname(os.path.abspath(__file__))
CORPUS_D = os.path.join(COUNTRY, "corpus.d")
CORPUS_JSON = os.path.join(COUNTRY, "corpus.json")
FLAGS = ("--install", "--write")
_allowed = False


def _flag(argv) -> bool:
    return any(f in (argv or ()) for f in FLAGS)


def allowed(argv=None) -> bool:
    return _allowed or _flag(argv) or _flag(sys.argv)


def default_dir() -> str:
    """The running driver's folder + '/.tmp'."""
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] or ".")), ".tmp")


def out_dir(argv, corpus_dir: str) -> str:
    """--out-dir DIR if given; corpus_dir with --install/--write; else the driver's .tmp."""
    global _allowed
    if _flag(argv):
        _allowed = True
    if "--out-dir" in argv:
        return argv[argv.index("--out-dir") + 1]
    return corpus_dir if _flag(argv) else default_dir()


def out_file(argv, corpus_path: str, flag: str = "--out") -> str:
    """--out FILE if given; corpus_path with --install/--write; else the driver's .tmp/<name>."""
    global _allowed
    if _flag(argv):
        _allowed = True
    if flag in argv:
        return argv[argv.index(flag) + 1]
    return corpus_path if _flag(argv) else os.path.join(default_dir(), os.path.basename(corpus_path))


def installed(path: str) -> bool:
    p = os.path.normcase(os.path.abspath(path))
    return p == os.path.normcase(CORPUS_JSON) or p.startswith(os.path.normcase(CORPUS_D) + os.sep)


def guard(path: str, argv=None) -> None:
    """Stop before writing into corpus.d / corpus.json without --install or --write."""
    if installed(path) and not allowed(argv):
        raise SystemExit(f"outguard: refusing to write {path}: the installed corpus is written only with --install "
                         f"(or --write); without it parts go to the driver's .tmp ({default_dir()}).")
