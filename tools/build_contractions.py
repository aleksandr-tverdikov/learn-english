#!/usr/bin/env python3
"""Assemble the contraction dictionary from tools/contractions/groups/*.json.

One tier only: contractions are a closed set, so there is no coverage pass to run
against a word list. Files this script no longer writes are deleted, and a duplicate
headword has its distinct senses merged rather than dropped.

CON_SRC and CON_CAT override the source and output directories, for testing.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'contractions'))
from lib import ROOT
from gen_contractions import render
from validate import check

SRC = os.environ.get('CON_SRC') or os.path.join(ROOT, 'tools', 'contractions')
CAT = os.environ.get('CON_CAT') or os.path.join(ROOT, 'grammar/02-contractions/catalog')


def write(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← Contractions](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    open(path, 'w').write('\n'.join(head) + '\n\n---\n\n'.join(render(e) for e in entries) + '\n')
    print(f'{os.path.basename(path):<34}{len(entries):>5} entries')


def load(path, problems):
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as exc:
        problems.append(f'{os.path.basename(path)}: BAD JSON ({exc})')
        return []
    good = []
    for e in data if isinstance(data, list) else []:
        p = check([e])
        if p:
            problems.append(f'{os.path.basename(path)}: {p[0]}' + (f' (+{len(p) - 1} more)' if len(p) > 1 else ''))
            continue
        good.append(e)
    return good


def words(text):
    return {w for w in re.findall(r'[a-z]+', text.lower()) if len(w) > 3}


def merge(into, other):
    added = 0
    for s in other['senses']:
        w = words(s['gloss'])
        if not any(s['gloss'].strip().lower() == t['gloss'].strip().lower()
                   or (w and len(w & words(t['gloss'])) / len(w) >= 0.5) for t in into['senses']):
            into['senses'].append(s); added += 1
    return added


def main():
    os.makedirs(CAT, exist_ok=True)
    groups = json.load(open(os.path.join(SRC, 'groups.json'), encoding='utf-8'))
    problems, seen, merged, written, total = [], {}, 0, set(), 0
    for g in groups:
        path = os.path.join(SRC, 'groups', f"{g['num']}-{g['slug']}.json")
        if not os.path.exists(path):
            problems.append(f"{g['num']}-{g['slug']}: not written yet")
            continue
        order = {w.lower(): i for i, w in enumerate(g['words'])}
        kept = []
        for e in sorted(load(path, problems),
                        key=lambda e: (order.get(e['term'].lower(), len(order)), e['term'].lower())):
            low = e['term'].lower()
            if low in seen:
                merged += merge(seen[low], e); continue
            seen[low] = e; kept.append(e)
        if kept:
            name = f"{g['num']}-{g['slug']}.md"
            write(os.path.join(CAT, name), g['title'], g['lede'], g['intro'], kept)
            written.add(name); total += len(kept)

    for f in glob.glob(os.path.join(CAT, '[0-9]*.md')):
        base = os.path.basename(f)
        if base not in written:
            os.remove(f)
            for sib in (f[:-3] + '.html', os.path.join(CAT, 'data', base[:-3] + '.json')):
                if os.path.exists(sib):
                    os.remove(sib)
            print(f'removed stale {base}')

    multi = sum(1 for e in seen.values() if len(e['senses']) > 1)
    print(f'\nwrote {len(written)} files, {total} contractions, {multi} with more than one expansion')
    if merged:
        print(f'merged {merged} senses from duplicate headwords')
    if problems:
        print(f'{len(problems)} problem(s):')
        for p in problems[:15]:
            print('   ', p)


if __name__ == '__main__':
    main()
