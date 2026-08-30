#!/usr/bin/env python3
"""Verify every relative link and anchor in the library, in both Markdown and HTML."""
import os, re, sys, glob
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, slugify

os.chdir(ROOT)
anchors = defaultdict(set)
MD = [f for f in glob.glob('**/*.md', recursive=True) if not f.startswith('tools/')]
for f in MD:
    src = open(f).read()
    seen = defaultdict(int)
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*$', src, re.M):
        b = slugify(h); n = seen[b]; seen[b] += 1
        anchors[f].add(b if n == 0 else f'{b}-{n}')
    for m in re.findall(r'(?:id|name)="([^"]+)"', src):   # explicit <a id> anchors, as GitHub honors
        anchors[f].add(m)

n = broken = dangling = 0
for f in MD:
    for p, a in re.findall(r'\]\(([^)#\s]*)(?:#([^)\s]+))?\)', open(f).read()):
        if p.startswith(('http', 'mailto')): continue
        n += 1
        t = os.path.normpath(os.path.join(os.path.dirname(f), p)) if p else f
        if p and not os.path.exists(t):
            broken += 1; print(f'  BROKEN md   {f} -> {p}')
        elif a and t.endswith('.md') and os.path.exists(t) and a not in anchors.get(t, set()):
            dangling += 1; print(f'  DANGLING    {f} -> {p}#{a}')

hn = hb = 0
for f in [x for x in glob.glob('**/*.html', recursive=True) if not x.startswith('tools/')]:
    for h in re.findall(r'href="([^"]+)"', open(f).read()):
        if h.startswith(('http', 'mailto', 'data:', '#')): continue
        path = h.split('#')[0]
        if not path: continue
        hn += 1
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), path))):
            hb += 1; print(f'  BROKEN html {f} -> {h}')

unbal = sum(1 for f in MD
            for l in open(f) if l.count('**') % 2)
print(f'markdown {n} links, {broken} broken, {dangling} dangling')
print(f'html     {hn} links, {hb} broken')
print(f'unbalanced ** lines: {unbal}')
_fail = broken or hb

# --- prose counts must match the live dictionaries -------------------------------
import glob as _glob
from lib import parse_catalog_file as _parse
from catalogs import CATALOGS as _CATS
_WORD = {'02-pronouns': 'pronouns', '06-prepositions': 'prepositions',
         '07-conjunctions': 'conjunctions', '08-interjections': 'interjections',
         '09-determiners': 'determiners', 'reporting-verbs': 'reporting verbs'}
_live = {}
for _c in _CATS:
    if os.path.isdir(_c['dir']):
        _live[_WORD.get(_c['slug'], _c['slug'])] = sum(
            len(_parse(f)) for f in _glob.glob(f"{_c['dir']}/[0-9]*.md"))
_bydir = {}
for _c in _CATS:
    if os.path.isdir(_c['dir']):
        _bydir[os.path.normpath(_c['dir'])] = sum(
            len(_parse(f)) for f in _glob.glob(f"{_c['dir']}/[0-9]*.md"))
_stale = 0
for _f in [f for f in _glob.glob('**/*.md', recursive=True) if not f.startswith('tools/')]:
    _src = open(_f).read()
    for _m in re.finditer(r'\[([\d,]+) entries\]\(([^)]*catalog/README\.md)\)', _src):
        _t = os.path.normpath(os.path.join(os.path.dirname(_f), os.path.dirname(_m.group(2))))
        if _t in _bydir and int(_m.group(1).replace(',', '')) != _bydir[_t]:
            _stale += 1
            print(f'  STALE COUNT {_f}: "{_m.group(1)} entries" -> {_bydir[_t]} ({_t})')
    for _w, _n in _live.items():
        for _m in re.finditer(r'\b([\d,]{2,6})\s+' + re.escape(_w) + r'\b', _src):
            if int(_m.group(1).replace(',', '')) != _n:
                _stale += 1
                print(f'  STALE COUNT {_f}: "{_m.group(1)} {_w}" but {_n} on disk')
print(f'prose counts: {_stale} stale')
sys.exit(1 if (_fail or _stale) else 0)
