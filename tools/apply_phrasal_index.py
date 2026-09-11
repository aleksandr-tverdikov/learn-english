#!/usr/bin/env python3
"""Give every irregular verb a Phrasal verbs line listing what is built on it.

The phrasal and verb+preposition files each name their base verb; this inverts that
into base -> [phrasal, ...] and writes a `**Phrasal verbs:**` line into the base verb's
own entry, just before its See also. Idempotent: an existing line is replaced.

Without this you can only go from `get up` to `get`. The useful direction for a learner
is the other one — open `get` and see everything built on it.
"""
import os, re, sys, glob
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, plain, parse_catalog_file

CAT = os.path.join(ROOT, 'parts-of-speech/03-verbs/catalog')
# base verbs are groups 01-13 (irregular) AND 23+ (regular). The regular tier did not
# exist when this script was written, so `call off` and `check in` had nowhere to be
# listed even once they were written - their bases are regular verbs.
BASE_FILES = sorted(glob.glob(f'{CAT}/0[0-9]-*.md') + glob.glob(f'{CAT}/1[0-3]-*.md')
                    + [f for f in glob.glob(f'{CAT}/[0-9]*.md')
                       if int(re.match(r'(\d+)', os.path.basename(f)).group(1)) >= 23])
DERIVED = sorted(glob.glob(f'{CAT}/1[4-9]-phrasal*.md') + glob.glob(f'{CAT}/2[01]-phrasal*.md')
                 + glob.glob(f'{CAT}/22-*.md'))

PHRASAL_LINE = re.compile(r'^\*\*Phrasal verbs:\*\*.*$')
SEE_ALSO = re.compile(r'^\*\*See also:\*\*')


def build_index():
    """base verb -> sorted [(phrase, 'file.md#anchor')]"""
    idx = defaultdict(list)
    for f in DERIVED:
        base_name = os.path.basename(f)
        for e in parse_catalog_file(f):
            # prefer the declared base verb; fall back to the first word of the phrase
            declared = plain(e['labels'].get('base verb', '')).split('·')[0].strip()
            declared = re.sub(r'\s*\(.*\)$', '', declared).strip().lower()
            base = declared.split()[0] if declared else e['term'].split()[0].lower()
            idx[base].append((e['term'], f'{base_name}#{e["anchor"]}'))
    for k in idx:
        idx[k] = sorted(set(idx[k]), key=lambda x: x[0].lower())
    return idx


def apply(idx):
    written = skipped = 0
    for f in BASE_FILES:
        lines = open(f).read().split('\n')
        out, i = [], 0
        while i < len(lines):
            m = re.match(r'^###\s+(.+?)\s*$', lines[i])
            if not m:
                out.append(lines[i]); i += 1
                continue
            term = plain(m.group(1)).lower()
            out.append(lines[i]); i += 1
            entry = []
            while i < len(lines) and not lines[i].startswith('### '):
                if PHRASAL_LINE.match(lines[i]):
                    # drop a previous run's line AND the blank this script put after it,
                    # otherwise blank lines accumulate on every rerun
                    i += 1
                    if i < len(lines) and not lines[i].strip():
                        i += 1
                    continue
                entry.append(lines[i])
                i += 1
            items = idx.get(term, [])
            if items:
                links = ' &middot; '.join(f'[{t}]({href})' for t, href in items)
                line = f'**Phrasal verbs:** {links}'
                at = next((k for k, l in enumerate(entry) if SEE_ALSO.match(l)), None)
                if at is None:
                    while entry and not entry[-1].strip():
                        entry.pop()
                    entry += ['', line, '']
                else:
                    entry.insert(at, line)
                    entry.insert(at + 1, '')
                written += 1
            else:
                skipped += 1
            out.extend(entry)
        open(f, 'w').write('\n'.join(out))
    return written, skipped


if __name__ == '__main__':
    idx = build_index()
    w, s = apply(idx)
    total = sum(len(v) for v in idx.values())
    print(f'indexed {total} derived verbs under {len(idx)} bases')
    print(f'wrote a Phrasal verbs line into {w} base entries ({s} bases have none)')
    top = sorted(idx.items(), key=lambda kv: -len(kv[1]))[:8]
    print('  most productive:', ', '.join(f'{k} ({len(v)})' for k, v in top))
