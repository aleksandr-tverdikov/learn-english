#!/usr/bin/env python3
"""Inject the grammatical-type labels into every verb entry.

Lexicographers write only `<catalog>/data/types/<slug>.json`:

    {"run": {"verb type": "action; also linking in *run low*",
             "transitivity": "both — intransitive (*she runs*), transitive (*run a business*)",
             "passive": "yes in the transitive senses — *the store is run by her sister*"}}

The lines are inserted at the end of the entry's label block, so they sit with Forms and
Register rather than in the prose. Idempotent: existing lines are replaced, never doubled.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, plain

FIELDS = ['Verb type', 'Transitivity', 'Passive']
OURS = re.compile(r'^\*\*(?:' + '|'.join(FIELDS) + r'):\*\*')
LABEL = re.compile(r'^\*\*(?!\d)[^*\n]+?:\*\*')
SEE_ALSO = re.compile(r'^\*\*See also:\*\*')


def apply_file(md_path, table):
    lines = open(md_path).read().split('\n')
    out, i, done, missing = [], 0, 0, []
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        m = re.match(r'^###\s+(.+?)\s*$', ln)
        if not m:
            i += 1
            continue
        term = plain(m.group(1))
        rec = table.get(term) or table.get(term.lower()) or {}
        i += 1
        block = []
        # gather the label block, dropping any previous run's lines
        while i < len(lines):
            l = lines[i]
            if l.startswith('### ') or SEE_ALSO.match(l):
                break
            if l.strip() and not LABEL.match(l):
                break
            if not OURS.match(l):
                block.append(l)
            i += 1
        while block and not block[-1].strip():
            block.pop()
        added = [f'**{f}:** {rec[k]}' for f, k in zip(FIELDS, [f.lower() for f in FIELDS])
                 if isinstance(rec.get(k), str) and rec[k].strip()]
        if added:
            done += 1
        else:
            missing.append(term)
        out.extend(block + added + [''])
    open(md_path, 'w').write('\n'.join(out))
    return done, missing


if __name__ == '__main__':
    targets = sys.argv[1:] or ['parts-of-speech/03-verbs/catalog']
    tot, miss, files = 0, [], 0
    for cat in targets:
        cat = os.path.join(ROOT, cat)
        for md in sorted(glob.glob(os.path.join(cat, '[0-9]*.md'))):
            slug = os.path.basename(md)[:-3]
            src = os.path.join(cat, 'data', 'types', slug + '.json')
            if not os.path.exists(src):
                continue
            try:
                table = json.load(open(src))
            except Exception as e:
                print(f'  BAD JSON {src}: {e}')
                continue
            table = {plain(k): v for k, v in table.items() if isinstance(v, dict)}
            d, m = apply_file(md, table)
            tot += d; miss += [f'{slug}: {t}' for t in m]; files += 1
            print(f'  {slug:<34}{d:>5} typed')
    print(f'\ntyped {tot} entries across {files} files')
    if miss:
        print(f'entries with no type data: {len(miss)}')
        for t in miss[:8]:
            print('   ', t)
