#!/usr/bin/env python3
"""Assemble phrasal verbs built on REGULAR bases.

The catalog's 925 existing phrasal verbs all sit on irregular bases - get, give,
take, put, come, go - because that is how the source spreadsheet was organized.
That left the whole regular-base family missing: no check in, no look up, no
figure out, no end up, no turn off.

These files are numbered 53+ and registered as derived in catalogs.py, so their
entries are nested inside their base verb's entry rather than listed as siblings,
the same treatment the irregular phrasal verbs get.
"""
import glob, json, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file

SRC = os.path.join(ROOT, 'tools', 'verbs')
CAT = os.path.join(ROOT, 'parts-of-speech/03-verbs/catalog')
START = 53
BANDS = [('a-c', 'abc'), ('d-f', 'def'), ('g-l', 'ghijkl'),
         ('m-p', 'mnop'), ('q-s', 'qrs'), ('t-z', 'tuvwxyz')]
REQUIRED = ('term', 'ipa', 'respell', 'ru', 'base', 'third', 'past', 'participle', 'ing', 'gloss')


def render(e):
    out = [f"### {e['term']}", '']
    out.append(f"**Pronunciation:** /{e['ipa'].strip('/')}/ &middot; *{e['respell']}*")
    out.append(f"**Русский:** {e['ru']}")
    out.append(f"**Base verb:** *{e['base']}*")
    if e.get('separable'):
        out.append(f"**Separable:** {e['separable']}")
    out.append(f"**Forms:** *{e['term']}* &middot; *{e['past']}* &middot; *{e['participle']}*")
    out.append(f"**Third person:** *{e['third']}* &middot; **-ing form:** *{e['ing']}*")
    if e.get('transitivity'):
        out.append(f"**Transitivity:** {e['transitivity']}")
    out += ['', e['gloss'], '']
    for i, x in enumerate(e['examples'][:3], 1):
        out.append(f'{i}. {x}')
    return '\n'.join(out)


def main():
    # Must skip this script's OWN output. Reading 53-58 back in makes every entry
    # look like a duplicate on the second run, so the files are never regenerated and
    # any later fix to the renderer silently fails to apply.
    existing = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        n = int(re.match(r'(\d+)', os.path.basename(f)).group(1))
        if START <= n <= START + len(BANDS) - 1:
            continue
        for x in parse_catalog_file(f):
            existing.add(x['term'].lower())

    pool, problems = [], []
    for p in sorted(glob.glob(os.path.join(SRC, 'phrasal-*.json'))):
        try:
            data = json.load(open(p))
        except Exception as exc:
            problems.append(f'{os.path.basename(p)}: BAD JSON ({exc})'); continue
        for e in data if isinstance(data, list) else []:
            if not isinstance(e, dict):
                continue
            t = (e.get('term') or '').strip()
            if any(not (e.get(k) or '').strip() for k in REQUIRED):
                problems.append(f'{t or "?"}: missing a required field'); continue
            ex = [x for x in (e.get('examples') or []) if isinstance(x, str)][:3]
            if len(ex) < 3:
                problems.append(f'{t}: {len(ex)} examples'); continue
            e['examples'] = ex
            pool.append(e)

    # a phrasal verb with several meanings gets several entries, so the key is
    # term+gloss rather than term alone
    seen, kept = set(), []
    for e in pool:
        k = (e['term'].lower(), e['gloss'].strip().lower())
        if k in seen:
            problems.append(f"{e['term']}: duplicate sense"); continue
        if e['term'].lower() in existing and e['term'].lower() not in {x['term'].lower() for x in kept}:
            problems.append(f"{e['term']}: already in the catalog"); continue
        seen.add(k)
        kept.append(e)

    groups = defaultdict(list)
    for e in kept:
        first = e['term'][0].lower()
        for i, (name, letters) in enumerate(BANDS):
            if first in letters:
                groups[i].append(e); break

    files = total = 0
    for i, (name, _) in enumerate(BANDS):
        g = sorted(groups.get(i, []), key=lambda e: (e['term'].lower(), e['gloss']))
        if not g:
            continue
        body = '\n\n---\n\n'.join(render(e) for e in g)
        head = [f'# Phrasal verbs on regular bases: {name.upper()}', '',
                f'> Phrasal verbs built on regular verbs — *check in*, *look up*, *figure out* — '
                f'headwords {name.upper()}.', '',
                '[← The grammar of verbs](../README.md) &middot; [All groups](README.md)', '',
                'The catalog\'s other 925 phrasal verbs are all built on **irregular** bases — '
                '*get*, *give*, *take*, *put*, *come*, *go* — because that is how the source '
                'material was organized. That left out the whole regular-base family, including '
                'some of the commonest phrasal verbs in English.\n\n'
                'Each entry names its **base verb** and says whether it is **separable**, which '
                'is the hardest thing about phrasal verbs: *turn it off* and *turn off the light* '
                'are both fine, but *look after the kids* can never become ✗ *look the kids '
                'after*. A phrasal verb with several distinct meanings gets one entry per '
                'meaning, because they are different verbs.', '', '---', '']
        open(os.path.join(CAT, f'{START + i}-phrasal-regular-{name}.md'), 'w').write(
            '\n'.join(head) + body + '\n')
        print(f'{START + i}-phrasal-regular-{name}.md  {len(g)} entries')
        files += 1; total += len(g)

    print(f'\nwrote {files} files, {total} phrasal verbs on regular bases')
    if problems:
        print(f'dropped {len(problems)}:')
        for p in problems[:10]:
            print('   ', p)


if __name__ == '__main__':
    main()
