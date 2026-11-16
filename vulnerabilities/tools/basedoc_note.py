"""basedoc_note.py <dir> <page stem e.g. ley_0906_2004> <article> <ruling e.g. C-519-07>: prints the notes of that article
that mention the ruling (the page and its js must be downloaded into <dir> as <stem><part>.html / .js)."""
import glob, html, os, re, sys

d, stem, art, rul = sys.argv[1:5]
for f in sorted(glob.glob(os.path.join(d, stem + "*.html"))):
    s = open(f, encoding="latin1").read()
    m = re.search(r'name="%s"' % re.escape(art), s)
    if not m:
        continue
    seg = s[m.start(): m.start() + 20000]
    nxt = re.search(r'class="bookmarkaj" name="', seg[20:])
    seg = seg[: 20 + nxt.start()] if nxt else seg
    print("==", os.path.basename(f), "text:", re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", seg)))[:600])
    js = f[:-5] + ".js"
    if not os.path.exists(js):
        print("no js"); continue
    j = open(js, encoding="latin1").read()
    for n in re.findall(r"insRow(\d+)\(\)", seg):
        a = j.find("function insRow%s(" % n); b = j.find("var z=", a)
        t = j[a:b]
        t = t.replace("<S>", "[[").replace("</S>", "]]").replace("<s>", "[[").replace("</s>", "]]")
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
        if rul in t or "Texto original" in t or "Legislaci" in t:
            print("  note", n, ":", t[:1500])
