#!/usr/bin/env python3
"""Assemble the adjective dictionary from the JSON in tools/adjectives/.

Two tiers, one entry shape (tools/adjectives/FORMAT.md):

    groups/<NN>-<slug>.json   the grammar tier, one file per group -> NN-<slug>.md
    core/add-<NN>.json        the WordNet triage pass            -> 30+ A-Z files

A headword lives in one file. When the same word arrives twice its distinct senses are
merged in rather than dropped, and band files this script no longer writes are deleted -
the two bugs the noun and verb builds each had once.

The 248 adjective + preposition patterns live in the preposition dictionary
(15-dependent-adjectives.md). Rather than copy them, each adjective gets a
"Preposition patterns" line linking to its own, sorted so the build stays idempotent.

ADJ_SRC and ADJ_CAT override the source and output directories, for testing.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'adjectives'))
from lib import ROOT, parse_catalog_file
from gen_adjectives import render
from validate import check

SRC = os.environ.get('ADJ_SRC') or os.path.join(ROOT, 'tools', 'adjectives')
CAT = os.environ.get('ADJ_CAT') or os.path.join(ROOT, 'parts-of-speech/04-adjectives/catalog')
PATTERNS = os.path.join(ROOT, 'parts-of-speech/06-prepositions/catalog/15-dependent-adjectives.md')
CORE_START = 30   # 17-29 left free for hand-shaped groups added later
BAND = 400


def write(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← The grammar of adjectives](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    body = '\n\n---\n\n'.join(render(e) for e in entries)
    open(path, 'w').write('\n'.join(head) + body + '\n')
    print(f'{os.path.basename(path):<44}{len(entries):>5} entries')


def load(path, problems):
    """Entries that pass the validator. A bad entry is reported and skipped, not fatal."""
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
    """Add the senses of `other` that `into` lacks. Returns how many were added."""
    added = 0
    for s in other['senses']:
        w = words(s['gloss'])
        dup = any(s['gloss'].strip().lower() == t['gloss'].strip().lower()
                  or (w and len(w & words(t['gloss'])) / len(w) >= 0.5)
                  for t in into['senses'])
        if not dup:
            into['senses'].append(s)
            added += 1
    for k in ('form', 'contrast', 'takes', 'opposite'):
        if not (into.get(k) or '').strip() and (other.get(k) or '').strip():
            into[k] = other[k]
    return added


def letter(term):
    return (re.sub(r'^[^a-z]+', '', term.lower())[:1] or 'a')


def pattern_index():
    """adjective -> sorted markdown links to its preposition patterns."""
    idx = {}
    if not os.path.exists(PATTERNS):
        return idx
    rel = os.path.relpath(PATTERNS, CAT)
    for e in parse_catalog_file(PATTERNS):
        for piece in e['term'].split(','):
            piece = piece.strip()
            if ' ' not in piece:
                continue
            adj = piece.rsplit(' ', 1)[0].lower()
            idx.setdefault(adj, set()).add((piece, e['anchor']))
    return {k: ' &middot; '.join(f'[{t}]({rel}#{a})' for t, a in sorted(v, key=lambda x: (x[0].lower(), x[1])))
            for k, v in idx.items()}


def main():
    os.makedirs(CAT, exist_ok=True)
    groups = json.load(open(os.path.join(SRC, 'groups.json'), encoding='utf-8'))
    problems, seen, merged = [], {}, 0

    tier1 = []
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
                merged += merge(seen[low], e)
                continue
            seen[low] = e
            kept.append(e)
        tier1.append((g, kept))

    pool = []
    for path in sorted(glob.glob(os.path.join(SRC, 'core', 'add-*.json'))):
        pool += load(path, problems)
    core = []
    for e in sorted(pool, key=lambda e: (letter(e['term']), e['term'].lower())):
        low = e['term'].lower()
        if low in seen:
            merged += merge(seen[low], e)
            continue
        seen[low] = e
        core.append(e)

    links = pattern_index()
    linked = 0
    for low, e in seen.items():
        if low in links:
            e['_patterns'] = links[low]
            linked += 1

    # write only after every source is loaded: a core slice may add senses to a grammar entry
    written = set()
    for g, kept in tier1:
        if kept:
            name = f"{g['num']}-{g['slug']}.md"
            write(os.path.join(CAT, name), g['title'], g['lede'], g['intro'], kept)
            written.add(name)

    bands, cur = [], []
    for e in core:
        if cur and len(cur) >= BAND and letter(e['term']) != letter(cur[-1]['term']):
            bands.append(cur)
            cur = []
        cur.append(e)
    if cur:
        bands.append(cur)
    for i, b in enumerate(bands):
        lo, hi = letter(b[0]['term']).upper(), letter(b[-1]['term']).upper()
        span = lo if lo == hi else f'{lo}–{hi}'
        name = f"{CORE_START + i}-more-adjectives-{span.replace('–', '-').lower()}.md"
        write(os.path.join(CAT, name), f'More adjectives: {span}',
              f'Adjectives {span} beyond the grammar groups — the everyday adjectives that a '
              'triage of WordNet’s adjective lemmas showed a learner needs.',
              'Most English adjectives behave: they go before a noun or after *be*, and they '
              'compare with *-er* or *more*. These are those — but each still says how it '
              'compares, where it can stand, and what it takes. WordNet lists about twenty '
              'thousand adjectives; most of the rest are technical, archaic or British-only, '
              'and a triage pass left them out on purpose.',
              b)
        written.add(name)

    # band names come from content, so a grown pool renames files: remove the old generation
    for f in glob.glob(os.path.join(CAT, '[0-9]*.md')):
        base = os.path.basename(f)
        if base not in written:
            os.remove(f)
            for sib in (f[:-3] + '.html', os.path.join(CAT, 'data', base[:-3] + '.json')):
                if os.path.exists(sib):
                    os.remove(sib)
            print(f'removed stale {base}')

    t1 = sum(len(k) for _, k in tier1)
    multi = sum(1 for e in seen.values() if len(e['senses']) > 1)
    print(f'\nwrote {len(written)} files, {t1 + len(core)} adjectives '
          f'({t1} grammar tier, {len(core)} core), {multi} with more than one sense, '
          f'{linked} linked to their preposition patterns')
    if merged:
        print(f'merged {merged} senses from duplicate headwords')
    if problems:
        print(f'{len(problems)} problem(s):')
        for p in problems[:15]:
            print('   ', p)


if __name__ == '__main__':
    main()
