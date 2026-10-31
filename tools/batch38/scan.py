"""List rulings / amendment boxes and inline markers on batch pages. Usage: scan.py page..."""
import sys, re
sys.argv = ['x', 'x', 'x'] + sys.argv[1:]
exec(open(__file__.replace('scan.py', 'show.py'), encoding='utf-8').read().split('for u in')[0])
for pg in sys.argv[3:]:
    for u in P.doc_units(pg):
        for it in u['items']:
            if it[0] == 'box' and 'Doctrina' not in it[1] and 'Proyecto' not in it[1]:
                t = E.plain(it[2])
                if re.search(r'INEXEQUIBLE|derogad|modificad|adicionad|suspend|sustitu', t, re.I):
                    print(pg, u['name'], it[1], ':', t[:400])
            if it[0] == 'p':
                for m in re.findall(r'&lt;(?:[^&]|&[a-z]+;){3,200}?&gt;', it[1]):
                    if not re.search(r'exequible', m, re.I):
                        print(pg, u['name'], 'MARK', m[:200])
