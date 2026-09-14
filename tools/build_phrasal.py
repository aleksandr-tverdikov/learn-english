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
IRR_START = 65   # phrasal verbs on IRREGULAR bases that groups 14-22 never covered
BANDS = [('a-c', 'abc'), ('d-f', 'def'), ('g-l', 'ghijkl'),
         ('m-p', 'mnop'), ('q-s', 'qrs'), ('t-z', 'tuvwxyz')]
IRR_BANDS = [('a-l', 'abcdefghijkl'), ('m-z', 'mnopqrstuvwxyz')]
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


def collect(sources, own_range):
    """Read the JSON sources and drop anything already in the catalog.

    `own_range` is the block of file numbers this pass writes. It must be skipped
    when scanning for existing terms: reading its own output back in makes every
    entry look like a duplicate on the second run, so the files are never
    regenerated and any later fix to the renderer silently fails to apply.
    """
    existing = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        n = int(re.match(r'(\d+)', os.path.basename(f)).group(1))
        if n in own_range:
            continue
        for x in parse_catalog_file(f):
            existing.add(x['term'].lower())

    pool, problems = [], []
    for p in sources:
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
    return kept, problems


def emit(kept, start, bands, name_fmt, title_fmt, lede_fmt, intro):
    groups = defaultdict(list)
    for e in kept:
        first = e['term'][0].lower()
        for i, (name, letters) in enumerate(bands):
            if first in letters:
                groups[i].append(e); break

    files = total = 0
    for i, (name, _) in enumerate(bands):
        g = sorted(groups.get(i, []), key=lambda e: (e['term'].lower(), e['gloss']))
        if not g:
            continue
        body = '\n\n---\n\n'.join(render(e) for e in g)
        head = [title_fmt.format(band=name.upper()), '',
                lede_fmt.format(band=name.upper()), '',
                '[← The grammar of verbs](../README.md) &middot; [All groups](README.md)', '',
                intro, '', '---', '']
        fn = name_fmt.format(num=start + i, band=name)
        open(os.path.join(CAT, fn), 'w').write('\n'.join(head) + body + '\n')
        print(f'{fn}  {len(g)} entries')
        files += 1; total += len(g)
    return files, total


REG_INTRO = (
    "The catalog's other 925 phrasal verbs are all built on **irregular** bases — "
    "*get*, *give*, *take*, *put*, *come*, *go* — because that is how the source "
    "material was organized. That left out the whole regular-base family, including "
    "some of the commonest phrasal verbs in English.\n\n"
    "Each entry names its **base verb** and says whether it is **separable**, which "
    "is the hardest thing about phrasal verbs: *turn it off* and *turn off the light* "
    "are both fine, but *look after the kids* can never become ✗ *look the kids "
    "after*. A phrasal verb with several distinct meanings gets one entry per "
    "meaning, because they are different verbs.")

IRR_INTRO = (
    "Groups 14-22 cover the phrasal verbs on irregular bases that came from the "
    "original source material. Checking the catalog against a full WordNet verb list "
    "turned up a further set it had never included — *fall through*, *hang about*, "
    "*stand over*, *read up* — and these are those.\n\n"
    "Each entry names its **base verb** and says whether it is **separable**. Because "
    "the base is irregular, the past and the participle are worth reading twice: "
    "*read up* → *read up* → *read up* looks unchanged but is not pronounced that way, "
    "and *sew up* → *sewed up* → *sewn up* changes only in the participle.")


def main():
    reg_sources = [p for p in sorted(glob.glob(os.path.join(SRC, 'phrasal-*.json')))
                   if not os.path.basename(p).startswith('phrasal-irr-')]
    irr_sources = sorted(glob.glob(os.path.join(SRC, 'phrasal-irr-*.json')))

    kept, problems = collect(reg_sources, range(START, START + len(BANDS)))
    f1, t1 = emit(kept, START, BANDS, '{num}-phrasal-regular-{band}.md',
                  '# Phrasal verbs on regular bases: {band}',
                  '> Phrasal verbs built on regular verbs — *check in*, *look up*, *figure out* — '
                  'headwords {band}.', REG_INTRO)
    print(f'\nwrote {f1} files, {t1} phrasal verbs on regular bases')

    f2 = t2 = 0
    if irr_sources:
        kept2, problems2 = collect(irr_sources, range(IRR_START, IRR_START + len(IRR_BANDS)))
        problems += problems2
        f2, t2 = emit(kept2, IRR_START, IRR_BANDS, '{num}-phrasal-irregular-more-{band}.md',
                      '# More phrasal verbs on irregular bases: {band}',
                      '> Phrasal verbs on irregular bases that groups 14-22 missed — headwords {band}.',
                      IRR_INTRO)
        print(f'wrote {f2} files, {t2} more phrasal verbs on irregular bases')

    if problems:
        print(f'dropped {len(problems)}:')
        for p in problems[:10]:
            print('   ', p)


if __name__ == '__main__':
    main()
