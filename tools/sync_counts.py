#!/usr/bin/env python3
"""Rewrite dictionary counts in prose so they match what is actually on disk.

Two patterns are recognized:
    [1,602 entries](path/to/catalog/README.md)   <- count resolved from the link target
    442 pronouns                                 <- count resolved from the class name
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file
from catalogs import CATALOGS

os.chdir(ROOT)
WORD = {'02-pronouns': 'pronouns', '06-prepositions': 'prepositions',
        '07-conjunctions': 'conjunctions', '08-interjections': 'interjections',
        '09-determiners': 'determiners', 'reporting-verbs': 'reporting verbs'}
live, by_dir = {}, {}
for c in CATALOGS:
    if not os.path.isdir(c['dir']):
        continue
    n = sum(len(parse_catalog_file(f)) for f in glob.glob(f"{c['dir']}/[0-9]*.md"))
    live[WORD.get(c['slug'], c['slug'])] = n
    by_dir[os.path.normpath(c['dir'])] = n

fixed = 0
for f in [x for x in glob.glob('**/*.md', recursive=True) if not x.startswith('tools/')]:
    src = out = open(f).read()

    def by_link(m):
        global fixed
        target = os.path.normpath(os.path.join(os.path.dirname(f), os.path.dirname(m.group(2))))
        n = by_dir.get(target)
        if n is None or int(m.group(1).replace(',', '')) == n:
            return m.group(0)
        fixed += 1
        return f'[{n:,} entries]({m.group(2)})'
    out = re.sub(r'\[([\d,]+) entries\]\(([^)]*catalog/README\.md)\)', by_link, out)

    for w, n in live.items():
        def by_word(m, _n=n, _w=w):
            global fixed
            if int(m.group(1).replace(',', '')) == _n:
                return m.group(0)
            fixed += 1
            return f'{_n:,} {_w}'
        out = re.sub(r'\b([\d,]{2,6})\s+' + re.escape(w) + r'\b', by_word, out)

    if out != src:
        open(f, 'w').write(out)
print(f'synced {fixed} stale counts')
