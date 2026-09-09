#!/usr/bin/env python3
"""Measure the noun dictionary against the WordNet noun list, and emit the gap.

Source: https://gist.github.com/trag1c/f74b2ab3589bc4ce5706f934616f6195
40,940 nouns pulled from WordNet, one per line. It carries no pronunciation,
no definition and no translation, so it cannot supply dictionary content - but
it is an excellent *checklist*, which is what it is used for here.

Two things it is NOT:

  * a target. Most of it is proper nouns (aachen, kerouac, switzerland), Latin
    taxonomy (hydrochoerus, synentognathi), and technical jargon
    (hypobetalipoproteinemia). A learner needs none of it.
  * a superset. Its generator excluded anything containing a space, so every
    multi-word noun a learner actually needs - washing machine, garage sale,
    toilet paper - is absent from it and present here.

The filters below are deliberately blunt, and their output is NOT a count of
words worth writing. They cannot detect proper nouns, because the source list is
lowercased - `aachen`, `abidjan` and `abelard` survive every string test that
`abacus` and `abbey` survive. Obsolete units (`abfarad`, `abcoulomb`) and rare
medical terms slip through too.

So the filtered list is a *worklist for judgment*, not a target. It is sliced
alphabetically and handed to writers whose actual job is to reject most of it.
Reporting its length as a gap figure would be misleading, so main() says so.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file

WORDNET = os.path.join(ROOT, 'tools', 'core', 'wordnet-nouns.txt')
CAT = os.path.join(ROOT, 'parts-of-speech/01-nouns/catalog')

# suffixes that mark scientific, medical or taxonomic vocabulary
JARGON = re.compile(r'(aceae|idae|inae|ales|phyta|zoa|itis|osis|emia|aemia|'
                    r'ectomy|otomy|ostomy|plasty|pathy|ology|ologist|'
                    r'ase|ide|ine|ium|yl|yne)$')
# strings that are almost always proper nouns in WordNet
PROPERISH = re.compile(r'(ia|land|shire|burg|ville|stan|opolis)$')


def ours():
    out = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        for e in parse_catalog_file(f):
            out.add(e['term'].lower())
    return out


def plausible(w):
    """cheap test for 'could a learner meet this word'"""
    if len(w) > 12 or len(w) < 3:
        return False
    if not w.isalpha():          # drops hyphens and apostrophes
        return False
    if JARGON.search(w):
        return False
    return True


def main():
    wn = {w.strip().lower() for w in open(WORDNET) if w.strip()}
    have = ours()
    missing = wn - have
    extra = have - wn

    useful = sorted(w for w in missing if plausible(w))
    likely_proper = sum(1 for w in missing if PROPERISH.search(w))

    print(f'WordNet list        {len(wn):>7,}')
    print(f'our dictionary      {len(have):>7,}')
    print(f'  covered by us     {len(wn & have):>7,}  ({100*len(wn & have)/len(wn):.0f}% of WordNet)')
    print(f'  ours it lacks     {len(extra):>7,}  (mostly multi-word compounds)')
    print()
    print(f'not yet covered     {len(missing):>7,}')
    print(f'  after filtering   {len(useful):>7,}  <- worklist for judgment, NOT a target')
    print(f'  dropped as jargon/proper/too long/too short: {len(missing)-len(useful):,}')
    print(f'  (of which ~{likely_proper:,} match place-name patterns)')

    print()
    print('  NOTE: that filtered number is a worklist, not a target. It cannot')
    print('  detect proper nouns - the source is lowercased, so aachen, abidjan')
    print('  and abelard pass every test abacus and abbey pass. Writers reject.')

    out = os.path.join(ROOT, 'tools', 'core', 'gap-list.txt')
    open(out, 'w').write('\n'.join(useful) + '\n')

    # alphabetical slices, one per writing agent
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    size = (len(useful) + n - 1) // n
    d = os.path.join(ROOT, 'tools', 'core', 'slices')
    os.makedirs(d, exist_ok=True)
    for old in glob.glob(f'{d}/*.txt'):
        os.remove(old)
    for i in range(n):
        chunk = useful[i*size:(i+1)*size]
        if not chunk:
            continue
        open(f'{d}/slice-{i:02d}.txt', 'w').write('\n'.join(chunk) + '\n')
    print(f'\nwrote {out}')
    print(f'wrote {n} slices of ~{size} words to {d}')
    print(f'  slice-00 spans {useful[0]} .. {useful[min(size,len(useful))-1]}')


if __name__ == '__main__':
    main()
