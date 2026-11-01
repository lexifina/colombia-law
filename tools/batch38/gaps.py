"""For each 'gap' article in batch38/parse.log, the first paragraph's markers and the boxes' headings."""
import sys, re
sys.argv = ['x', 'x', 'x']
exec(open(__file__.replace('gaps.py', 'show.py'), encoding='utf-8').read().split('for u in')[0])
B8.PAGES.add('ley_1955_2019')
gaps = re.findall(r'gap art-(\d+)', open(__file__.replace('gaps.py', 'parse.log'), encoding='utf-8').read())
us = {u['name']: u for u in P.doc_units('ley_1955_2019')}
for g in gaps:
    u = us[str(int(g))]
    p0 = next(it[1] for it in u['items'] if it[0] == 'p')
    print(int(g), '|', ' || '.join(E.markers(p0))[:160])
    for it in u['items']:
        if it[0] == 'box' and it[1] in ('Legislación Anterior', 'Notas de Vigencia'):
            print('     ', it[1][:6], ':', E.plain(it[2])[:150].replace('\n', ' '))
