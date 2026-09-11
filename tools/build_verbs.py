#!/usr/bin/env python3
"""Assemble the core-verb catalog files from tools/verbs/*.json.

Mirrors build_core.py for nouns. Groups 1-22 of the verb catalog are the verbs
that misbehave - irregular forms, phrasal verbs, verb + preposition. Groups 23+
are the regular verbs that were never a category, which is why `work`, `need`,
`ask` and `explain` were absent from a dictionary of 1,291 verbs.

Anything already in groups 1-22 is dropped rather than duplicated: an irregular
verb's full entry always beats a lean one, and a phrasal verb belongs with its
base verb.
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file
from gen_verbs import build

SRC = os.path.join(ROOT, 'tools', 'verbs')
CAT = os.path.join(ROOT, 'parts-of-speech/03-verbs/catalog')
START = 23

ORDER = [
    ('motion-travel', 'motion and travel'), ('speech-communication', 'speech and communication'),
    ('thinking-knowing', 'thinking and knowing'), ('perception-senses', 'the senses'),
    ('emotion-feeling', 'emotion'), ('work-business', 'work and business'),
    ('making-building', 'making and building'), ('destroying-damaging', 'damage and repair'),
    ('giving-taking', 'giving and taking'), ('buying-selling', 'money and trade'),
    ('eating-drinking', 'eating and drinking'), ('cooking-food', 'cooking'),
    ('body-health', 'the body and health'), ('cleaning-household', 'cleaning and the home'),
    ('clothing-dressing', 'clothing'), ('learning-teaching', 'learning and teaching'),
    ('reading-writing', 'reading and writing'), ('social-relationships', 'relationships'),
    ('conflict-fighting', 'conflict'), ('law-crime', 'law and crime'),
    ('government-politics', 'government'), ('sport-games', 'sport and games'),
    ('art-music-performance', 'art and performance'), ('technology-computing', 'technology'),
    ('driving-transport', 'driving and transport'), ('farming-nature', 'farming and nature'),
    ('weather-natural', 'weather and natural processes'), ('change-growth', 'change and growth'),
    ('starting-stopping', 'starting and stopping'), ('helping-caring', 'helping and caring'),
]

REQUIRED = ('term', 'ipa', 'respell', 'ru', 'third', 'past', 'participle', 'ing', 'gloss')


def main():
    existing = set()
    for f in sorted(glob.glob(f'{CAT}/[0-9]*.md')):
        if '-core-' in os.path.basename(f):
            continue
        for e in parse_catalog_file(f):
            existing.add(e['term'].lower())

    seen, problems, files, total = set(), [], 0, 0
    for i, (slug, name) in enumerate(ORDER):
        src = os.path.join(SRC, slug + '.json')
        if not os.path.exists(src):
            continue
        try:
            data = json.load(open(src))
        except Exception as exc:
            problems.append(f'{slug}: BAD JSON ({exc})'); continue

        rows = []
        for e in data if isinstance(data, list) else []:
            if not isinstance(e, dict):
                continue
            t = (e.get('term') or '').strip()
            low = t.lower()
            if not t:
                continue
            if low in existing:
                problems.append(f'{slug}: "{t}" already in groups 1-22'); continue
            if low in seen:
                problems.append(f'{slug}: "{t}" duplicated'); continue
            if any(not (e.get(k) or '').strip() for k in REQUIRED):
                problems.append(f'{slug}: "{t}" missing a required field'); continue
            ex = [x for x in (e.get('examples') or []) if isinstance(x, str)][:3]
            if len(ex) < 3:
                problems.append(f'{slug}: "{t}" has {len(ex)} examples'); continue
            seen.add(low)
            rows.append((t, e['ipa'].strip('/'), e['respell'], e['ru'], e['third'],
                         e['past'], e['participle'], e['ing'],
                         e.get('transitivity') or '', e['gloss'], ex,
                         e.get('contrast') or None))
        if not rows:
            continue
        build(os.path.join(CAT, f'{START + i}-core-{slug}.md'),
              f'Core verbs: {name}',
              f'The everyday regular verbs of {name} — all four forms, pronunciation, '
              'Russian, and three examples that use more than one form.',
              'Groups 1–22 cover the verbs that **misbehave**: irregular forms, phrasal verbs, '
              'and verb + preposition patterns. This tier covers the regular verbs, which were '
              'never a category here — which is why a dictionary of 1,291 verbs had no *work*, '
              'no *need*, no *ask* and no *explain*.\n\n'
              'Regular does not mean effortless. The forms are still where learners fail: '
              '*carry → carried*, *stop → stopped*, *agree → agreed*. Every entry spells all '
              'four out, and a **Contrast** line appears wherever the spelling or a required '
              'preposition is the trap.',
              rows)
        files += 1; total += len(rows)

    print(f'\nwrote {files} core verb files, {total} entries')
    if problems:
        print(f'dropped {len(problems)}:')
        for p in problems[:12]:
            print('   ', p)


if __name__ == '__main__':
    main()
