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


def main():
    grammar = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        if '-core-' in os.path.basename(f):
            continue
        for e in parse_catalog_file(f):
            grammar.add(e['term'].lower())

    seen, problems, written, total = {}, [], 0, 0
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
                kept.append((e['term'], e['ipa'], e['respell'], e['ru'],
                             e.get('plural') or '', e['countability'],
                             e['gloss'], e['examples'], e.get('contrast') or None))
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

    print(f'\nwrote {written} core files, {total} entries')
    if problems:
        print(f'dropped {len(problems)} entries:')
        for p in problems[:25]:
            print('   ', p)
        if len(problems) > 25:
            print(f'    ... and {len(problems) - 25} more')


if __name__ == '__main__':
    main()
