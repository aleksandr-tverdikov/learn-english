#!/usr/bin/env python3
"""Assemble the core-vocabulary catalog files from tools/core/*.json.

The grammar tier (groups 1-23) is hand-written prose. This tier is authored as
structured JSON, one file per semantic field, and rendered here so the format
cannot drift and so duplicates can be resolved deterministically.

Rules, applied in this order and all logged rather than silent:
  * an entry whose term is already in the grammar tier is dropped - the full
    entry there always wins over a lean one here
  * a term appearing in two fields is kept in the first field only
  * an entry that fails validation is dropped and named

Idempotent: rerunning regenerates every file from the JSON.
"""
import glob, json, os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file
from gen_core import build

CORE = os.path.join(ROOT, 'tools', 'core')
CAT = os.path.join(ROOT, 'parts-of-speech/01-nouns/catalog')
START_NUM = 25          # groups 1-23 are the grammar tier, 24 is core-people

# field order fixes the file numbering; must match the workflow's FIELDS list
ORDER = [
    'body-parts', 'health-medicine', 'food-staples', 'fruit-vegetables',
    'meat-fish-dairy', 'drinks', 'cooking-kitchen', 'house-rooms', 'furniture',
    'household-objects', 'clothing', 'accessories-jewelry', 'tools-hardware',
    'materials-substances', 'nature-landscape', 'weather-sky', 'plants-trees',
    'mammals', 'birds', 'insects-reptiles', 'sea-life', 'time-calendar',
    'measurement', 'money-finance', 'business-commerce', 'work-office',
    'education-school', 'language-writing', 'books-media', 'art-music',
    'sport-games', 'transport-vehicles', 'travel-tourism', 'city-buildings',
    'law-crime', 'government-politics', 'war-military', 'religion-belief',
    'science-physics', 'technology-computing', 'communication-internet',
    'emotions-feelings', 'mind-thought', 'society-groups', 'events-celebrations',
    'shapes-colors', 'containers-packaging', 'agriculture-farming',
    'energy-industry', 'clothing-textiles',
    # wave 2 fields
    'restaurants-dining', 'shopping-retail', 'footwear',
    'hair-beauty', 'hygiene-bathroom', 'childcare-parenting',
    'pets-animal-care', 'hunting-fishing', 'camping-outdoors',
    'gardening', 'cleaning-laundry', 'safety-emergency',
    'construction-building', 'architecture-interiors', 'plumbing-heating',
    'roads-driving', 'aviation', 'maritime-shipping',
    'railways', 'printing-publishing', 'photography-film',
    'theatre-performance', 'literature-genres', 'mythology-folklore',
    'history-eras', 'geology-minerals', 'chemistry-elements',
    'biology-cells', 'ecology-environment', 'astronomy-space',
    'mathematics-terms', 'psychology-therapy', 'fitness-exercise',
    'music-genres',
]

TITLES = {
    'body-parts': 'the body', 'health-medicine': 'health and medicine',
    'food-staples': 'food and meals', 'fruit-vegetables': 'fruit and vegetables',
    'meat-fish-dairy': 'meat, fish, and dairy', 'drinks': 'drinks',
    'cooking-kitchen': 'cooking and the kitchen', 'house-rooms': 'the house',
    'furniture': 'furniture', 'household-objects': 'household objects',
    'clothing': 'clothing', 'accessories-jewelry': 'accessories and jewelry',
    'tools-hardware': 'tools and hardware', 'materials-substances': 'materials and substances',
    'nature-landscape': 'landscape and geography', 'weather-sky': 'weather and the sky',
    'plants-trees': 'plants and trees', 'mammals': 'mammals', 'birds': 'birds',
    'insects-reptiles': 'insects and reptiles', 'sea-life': 'sea life',
    'time-calendar': 'time and the calendar', 'measurement': 'measurement',
    'money-finance': 'money and finance', 'business-commerce': 'business and commerce',
    'work-office': 'work and the office', 'education-school': 'education',
    'language-writing': 'language and writing', 'books-media': 'books and media',
    'art-music': 'art and music', 'sport-games': 'sport and games',
    'transport-vehicles': 'transport and vehicles', 'travel-tourism': 'travel',
    'city-buildings': 'the city', 'law-crime': 'law and crime',
    'government-politics': 'government and politics', 'war-military': 'war and the military',
    'religion-belief': 'religion and belief', 'science-physics': 'science',
    'technology-computing': 'technology and computing',
    'communication-internet': 'communication and the internet',
    'emotions-feelings': 'emotions', 'mind-thought': 'mind and thought',
    'society-groups': 'society', 'events-celebrations': 'events and celebrations',
    'shapes-colors': 'shapes and colors', 'containers-packaging': 'containers and packaging',
    'agriculture-farming': 'farming', 'energy-industry': 'energy and industry',
    'clothing-textiles': 'fabric and textiles',
    'restaurants-dining': 'restaurants and dining out',
    'shopping-retail': 'shopping and retail',
    'footwear': 'footwear',
    'hair-beauty': 'hair and beauty',
    'hygiene-bathroom': 'hygiene and the bathroom',
    'childcare-parenting': 'babies and parenting',
    'pets-animal-care': 'pets and animal care',
    'hunting-fishing': 'hunting and fishing',
    'camping-outdoors': 'camping and the outdoors',
    'gardening': 'gardening',
    'cleaning-laundry': 'cleaning and laundry',
    'safety-emergency': 'safety and emergencies',
    'construction-building': 'construction',
    'architecture-interiors': 'architecture and interiors',
    'plumbing-heating': 'plumbing and heating',
    'roads-driving': 'roads and driving',
    'aviation': 'aviation',
    'maritime-shipping': 'ships and the sea',
    'railways': 'railways',
    'printing-publishing': 'printing and publishing',
    'photography-film': 'photography and film',
    'theatre-performance': 'theatre and performance',
    'literature-genres': 'literature',
    'mythology-folklore': 'mythology and folklore',
    'history-eras': 'history',
    'geology-minerals': 'geology and minerals',
    'chemistry-elements': 'chemistry',
    'biology-cells': 'biology',
    'ecology-environment': 'ecology and the environment',
    'astronomy-space': 'astronomy and space',
    'mathematics-terms': 'mathematics',
    'psychology-therapy': 'psychology and therapy',
    'fitness-exercise': 'fitness and exercise',
    'music-genres': 'music and recording',
}

COUNTS = {'countable', 'uncountable',
          'countable, and uncountable as a substance',
          'countable, and uncountable as food',
          'both — countable and uncountable with different meanings'}


def valid(e, seen, grammar, problems, slug):
    t = (e.get('term') or '').strip()
    if not t:
        problems.append(f'{slug}: entry with no term'); return False
    low = t.lower()
    if low in grammar:
        problems.append(f'{slug}: "{t}" already in the grammar tier'); return False
    if low in seen:
        problems.append(f'{slug}: "{t}" duplicated (kept in {seen[low]})'); return False
    for k in ('ipa', 'respell', 'ru', 'gloss'):
        if not (e.get(k) or '').strip():
            problems.append(f'{slug}: "{t}" missing {k}'); return False
    if '/' in e['ipa']:
        e['ipa'] = e['ipa'].strip('/')
    ex = e.get('examples') or []
    if len(ex) < 3:
        problems.append(f'{slug}: "{t}" has {len(ex)} examples'); return False
    e['examples'] = ex[:3]
    if e.get('countability') not in COUNTS:
        e['countability'] = 'uncountable' if not e.get('plural') else 'countable'
    return True


def extra_senses():
    """term -> [(gloss, ru, examples)] written by the sense-expansion pass.

    Merging recovered the senses that different fields happened to write. It
    could not recover a sense nobody wrote at all: `fracture` was only ever
    described as a broken bone, `pupil` only as a schoolchild. These files hold
    those missing meanings, written against the gloss already present so they
    do not repeat it.
    """
    out = defaultdict(list)
    for src in sorted(glob.glob(os.path.join(CORE, 'senses', 'add-*.json'))):
        try:
            data = json.load(open(src))
        except Exception:
            continue
        for row in data if isinstance(data, list) else []:
            if not isinstance(row, dict):
                continue
            t = (row.get('term') or '').strip().lower()
            for sn in row.get('senses') or []:
                g = (sn.get('gloss') or '').strip()
                ex = [x for x in (sn.get('examples') or []) if isinstance(x, str)][:3]
                if t and g and len(ex) == 3:
                    out[t].append((g, (sn.get('ru') or '').strip(), ex))
    return out


EXTRA = None
ORDERING = None
HOMOGRAPHS = None


def homographs():
    """Words spelled alike but pronounced differently, one entry per pronunciation.

    Every other entry in this dictionary carries a single IPA shared by all its
    senses, which is right for `bank` (both senses /bæŋk/) and wrong for `bass`,
    where the fish is /bæs/ and the low musical range /beɪs/. Those are two words
    that happen to share a spelling, so they get two entries.

    This is the one place a repeated headword is correct rather than a bug, so
    these terms are held out of the normal term dedupe and rendered together in
    their own group, where the contrast between the pronunciations is the point.
    """
    src = os.path.join(CORE, 'homographs.json')
    if not os.path.exists(src):
        return []
    try:
        data = json.load(open(src))
    except Exception:
        return []
    return [e for e in (data if isinstance(data, list) else []) if isinstance(e, dict)]


def build_homographs(grammar, problems):
    rows = []
    for e in HOMOGRAPHS:
        for k in ('term', 'ipa', 'respell', 'ru', 'gloss'):
            if not (e.get(k) or '').strip():
                problems.append(f"homograph {e.get('term','?')}: missing {k}")
                break
        else:
            ex = [x for x in (e.get('examples') or []) if isinstance(x, str)][:3]
            if len(ex) < 3:
                problems.append(f"homograph {e['term']}: {len(ex)} examples")
                continue
            rows.append((e['term'], e['ipa'].strip('/'), e['respell'], e['ru'],
                         e.get('plural') or '', e.get('countability') or 'countable',
                         e['gloss'], ex, e.get('contrast') or None, None))
    if not rows:
        return 0, 0
    rows.sort(key=lambda r: (r[0].lower(), r[1]))
    build(os.path.join(CAT, '130-core-homographs.md'),
          'Core vocabulary: words spelled alike, said differently',
          'One spelling, two pronunciations, two meanings — *bass* the fish and *bass* the '
          'low notes are different words that happen to look the same.',
          'Every other entry in this dictionary gives one pronunciation and lists its meanings '
          'underneath, because the meanings sound the same. These do not.\n\n'
          '*Bass* the fish is /bæs/ and *bass* the low musical range is /beɪs/. *Lead* the metal '
          'is /lɛd/ and *lead* meaning first place is /liːd/. Treating those as one entry with '
          'two senses would attach a pronunciation to a meaning it does not have, so each gets '
          'its own entry and each points at the other.\n\n'
          'Noun/verb pairs are deliberately excluded — *record*, *contrast*, *permit* shift '
          'stress between a noun and a verb, and this is a dictionary of nouns.',
          rows)
    return 1, len(rows)


def sense_order():
    """term -> [1-based sense positions] in the order they should be shown.

    Sense order came out of the build as an artifact: whichever field wrote the
    word first got sense 1, so `date` led with the fruit and `ball` with the
    formal dance. This holds a judged order instead.

    A permutation is applied only if it is exactly a rearrangement of the senses
    actually present. Anything else - wrong length, a missing or repeated index -
    is discarded rather than applied, because a bad permutation would silently
    drop or duplicate a meaning.
    """
    out = {}
    for src in sorted(glob.glob(os.path.join(CORE, 'order', 'set-*.json'))):
        try:
            data = json.load(open(src))
        except Exception:
            continue
        for row in data if isinstance(data, list) else []:
            if not isinstance(row, dict):
                continue
            t = (row.get('term') or '').strip().lower()
            o = row.get('order')
            if t and isinstance(o, list) and all(isinstance(x, int) for x in o):
                out[t] = o
    return out


def apply_order(term, senses, problems):
    o = (ORDERING or {}).get(term.lower())
    if not o:
        return senses
    if sorted(o) != list(range(1, len(senses) + 1)):
        problems.append(f'{term}: order {o} is not a permutation of {len(senses)} senses')
        return senses
    return [senses[i - 1] for i in o]


def sense_index():
    """term -> [(slug, entry)] across every source, in ORDER then gap order.

    A word written by several fields usually has several meanings. Keeping only
    the first field's version threw away 428 real senses - alarm as a feeling
    and alarm as a device, arrow the symbol and arrow the weapon, alcohol the
    intoxicant and alcohol the solvent. This collects them all so they can be
    merged into one entry instead.
    """
    idx = defaultdict(list)
    order = list(ORDER) + [os.path.basename(p)[:-5]
                           for p in sorted(glob.glob(os.path.join(CORE, 'gap-*.json')))]
    for slug in order:
        src = os.path.join(CORE, slug + '.json')
        if not os.path.exists(src):
            continue
        try:
            data = json.load(open(src))
        except Exception:
            continue
        if isinstance(data, dict):
            data = data.get('entries') or []
        for e in data:
            if isinstance(e, dict) and (e.get('term') or '').strip():
                idx[e['term'].lower()].append((slug, e))
    return idx


def distinct_sense(a, b):
    """Do two glosses describe materially different meanings?

    Word overlap is crude but it is the right kind of crude here: near-identical
    glosses of the same sense share most of their content words, while a bone
    fracture and a rock fracture share almost none.
    """
    wa = {w for w in a.lower().split() if len(w) > 3}
    wb = {w for w in b.lower().split() if len(w) > 3}
    if not wa or not wb:
        return False
    return len(wa & wb) / min(len(wa), len(wb)) < 0.5


MERGE_PROBLEMS = []


def merge(entries):
    """Fold [(slug, entry)] for one term into a single row for the renderer."""
    first = entries[0][1]
    senses, rus = [], []
    pool = [(None, e) for _, e in entries]
    for g, ru, ex in EXTRA.get(first['term'].lower(), []):
        pool.append((None, {'gloss': g, 'ru': ru, 'examples': ex}))
    for _, e in pool:
        g = (e.get('gloss') or '').strip()
        if not g:
            continue
        if any(not distinct_sense(g, sg) for sg, _, _ in senses):
            continue                              # same meaning said twice
        senses.append((g, (e.get('ru') or '').strip(), (e.get('examples') or [])[:3]))
        if e.get('ru') and e['ru'].strip() not in rus:
            rus.append(e['ru'].strip())
    senses = apply_order(first['term'], senses, MERGE_PROBLEMS)
    # the header must be rebuilt AFTER the reorder, not before: it is a summary of
    # the senses, so listing them in a different order than the entry does makes the
    # entry contradict its own headline
    rus = []
    for _, sru, _ in senses:
        if sru and sru not in rus:
            rus.append(sru)
    contrast = next((e.get('contrast') for _, e in entries if e.get('contrast')), None)
    ru = '; '.join(rus) if len(rus) > 1 else (rus[0] if rus else first.get('ru', ''))
    return (first['term'], first['ipa'], first['respell'], ru,
            first.get('plural') or '', first['countability'],
            senses[0][0] if senses else first.get('gloss', ''),
            senses[0][2] if senses else first.get('examples', []),
            contrast,
            senses if len(senses) > 1 else None)


def main():
    global EXTRA, ORDERING, HOMOGRAPHS
    EXTRA = extra_senses()
    ORDERING = sense_order()
    HOMOGRAPHS = homographs()

    grammar = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        if '-core-' in os.path.basename(f):
            continue
        for e in parse_catalog_file(f):
            grammar.add(e['term'].lower())

    idx = sense_index()
    seen, problems, written, total, multi = {}, [], 0, 0, 0
    for e in HOMOGRAPHS:                      # handled in their own group
        seen[(e.get('term') or '').lower()] = 'homographs' 
    for i, slug in enumerate(ORDER):
        src = os.path.join(CORE, slug + '.json')
        if not os.path.exists(src):
            continue
        try:
            data = json.load(open(src))
        except Exception as exc:
            problems.append(f'{slug}: BAD JSON ({exc})'); continue
        if isinstance(data, dict):
            data = data.get('entries') or []

        kept = []
        for e in data:
            if not isinstance(e, dict):
                continue
            if valid(e, seen, grammar, problems, slug):
                seen[e['term'].lower()] = slug
                row = merge(idx[e['term'].lower()])
                if row[9]:
                    multi += 1
                kept.append(row)
        if not kept:
            continue
        num = START_NUM + i
        name = TITLES.get(slug, slug.replace('-', ' '))
        build(os.path.join(CAT, f'{num}-core-{slug}.md'),
              f'Core vocabulary: {name}',
              f'The everyday nouns of {name} — pronunciation, Russian, plural, and three examples each.',
              'Part of the **core-vocabulary tier**. Groups 1–23 cover the nouns that misbehave; '
              'this tier covers the nouns you simply need to know. Entries are deliberately lean, '
              'because a regular countable noun has no grammatical story to tell. A **Contrast** '
              'line appears only where the word hides a genuine trap.\n\n'
              'Where a word in this field *does* misbehave, it lives in the grammar tier instead '
              'and is not repeated here.',
              kept)
        written += 1
        total += len(kept)

    gfiles, gentries = build_gap(seen, grammar, problems)
    written += gfiles
    total += gentries

    hfiles, hentries = build_homographs(grammar, problems)
    written += hfiles
    total += hentries

    print(f'\nwrote {written} core files, {total} entries')
    if multi:
        print(f'  {multi} entries carry more than one sense, merged from separate fields')
    if ORDERING:
        print(f'  {len(ORDERING)} entries have a judged sense order applied')
    if HOMOGRAPHS:
        print(f'  {hentries} homograph entries across {len({e["term"].lower() for e in HOMOGRAPHS})} spellings')
    for p in MERGE_PROBLEMS[:5]:
        print('   ', p)
    if gfiles:
        print(f'  of which {gfiles} A-Z files hold {gentries} entries from the gap pass')
    if problems:
        print(f'dropped {len(problems)} entries:')
        for p in problems[:25]:
            print('   ', p)
        if len(problems) > 25:
            print(f'    ... and {len(problems) - 25} more')


def build_gap(seen, grammar, problems):
    """Fold the alphabetical gap slices into a few readable A-Z files.

    The 40 slices are an artifact of how the work was divided among agents, not
    something a reader should ever see, so they collapse into a handful of
    ranges named by their initial letters.
    """
    entries = []
    for src in sorted(glob.glob(os.path.join(CORE, 'gap-*.json'))):
        try:
            data = json.load(open(src))
        except Exception as exc:
            problems.append(f'{os.path.basename(src)}: BAD JSON ({exc})')
            continue
        if isinstance(data, dict):
            data = data.get('entries') or []
        entries += [e for e in data if isinstance(e, dict)]
    if not entries:
        return 0, 0

    entries.sort(key=lambda e: (e.get('term') or '').lower())
    idx = sense_index()
    global EXTRA
    if EXTRA is None:
        EXTRA = extra_senses()
    global ORDERING
    if ORDERING is None:
        ORDERING = sense_order()
    kept = []
    for e in entries:
        if valid(e, seen, grammar, problems, 'gap'):
            seen[e['term'].lower()] = 'gap'
            kept.append(e)
    if not kept:
        return 0, 0

    # split into ranges of roughly equal size, cutting only between letters
    target = 400
    groups, cur, letter = [], [], kept[0]['term'][0].lower()
    for e in kept:
        l = e['term'][0].lower()
        if l != letter and len(cur) >= target:
            groups.append(cur)
            cur = []
        letter = l
        cur.append(e)
    if cur:
        groups.append(cur)

    num = 120
    for g in groups:
        lo, hi = g[0]['term'][0].upper(), g[-1]['term'][0].upper()
        span = lo if lo == hi else f'{lo}-{hi}'
        rows = [merge(idx[e['term'].lower()]) for e in g]
        build(os.path.join(CAT, f'{num}-core-more-{span.lower()}.md'),
              f'Core vocabulary: more nouns {span}',
              f'Further everyday nouns, {span} — what a coverage check against WordNet '
              'showed was still missing.',
              'Part of the **core-vocabulary tier**, gathered by checking the dictionary against a '
              '40,940-word WordNet noun list and writing entries for what was genuinely absent.\n\n'
              'Most of that list was not worth writing — proper nouns, Latin taxonomy, obsolete '
              'units and archaic terms — so these are the survivors of a deliberate rejection pass '
              'that threw out roughly six of every seven candidates, not the list itself.',
              rows)
        num += 1
    return len(groups), len(kept)


if __name__ == '__main__':
    main()
