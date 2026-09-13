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
WORD = {'01-nouns': 'nouns', '02-pronouns': 'pronouns', '06-prepositions': 'prepositions',
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
        """Resync a count whose link points at a catalog.

        Only the link form is safe to rewrite. A bare "1,291 verbs" in prose may be
        a historical statement - "a dictionary of 1,291 verbs had no work" - or a
        different catalog's count entirely, as in "the 313 verbs you can report
        with". The link target says which catalog is meant, so there is no guessing.
        The noun after the number is preserved: some tables say "entries", the verb
        row says "verbs".
        """
        global fixed
        target = os.path.normpath(os.path.join(os.path.dirname(f), os.path.dirname(m.group(3))))
        n = by_dir.get(target)
        if n is None or int(m.group(1).replace(',', '')) == n:
            return m.group(0)
        fixed += 1
        return f'[{n:,} {m.group(2)}]({m.group(3)})'
    out = re.sub(r'\[([\d,]+) (entries|verbs|nouns|words)\]\(([^)]*catalog/README\.md)\)',
                 by_link, out)

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
