#!/usr/bin/env python3
"""Check one adjective JSON file against tools/adjectives/FORMAT.md.

    python3 tools/adjectives/validate.py tools/adjectives/groups/02-ing-and-ed.json

The adverb validator's twin. Writers run it on their own file before finishing, so a
tag label that is really prose, a bare /e/, an unbalanced asterisk, or an entry whose
examples never show the comparative it lists is caught by the person who can fix it.
"""
import json, re, sys

TYPES = {'quality', 'emotion', 'evaluative', 'size', 'shape', 'age', 'color', 'material', 'origin',
         'classifying', 'participial', 'compound', 'emphasizing', 'quantity'}
POSITIONS = {'both', 'attributive only', 'predicative only', 'after the noun'}
COMPARISONS = {'-er/-est', 'more/most', '-er/-est or more/most', 'irregular', 'not gradable'}
WITH_FORMS = {'-er/-est', '-er/-est or more/most', 'irregular'}
REQUIRED = ('term', 'ipa', 'respell', 'ru', 'type', 'position', 'comparison')


def head(v):
    return re.split(r'[—(;,]|--| - ', re.sub(r'[*_]', '', v or ''))[0].strip().strip('.').lower()


def spans(text):
    return [s.strip().lower() for s in re.findall(r'\*([^*]+)\*', text)]


def check(entries):
    problems, seen = [], set()
    if not isinstance(entries, list):
        return ['file is not a JSON array']
    for i, e in enumerate(entries):
        t = (e.get('term') or '').strip() if isinstance(e, dict) else ''
        where = t or f'entry #{i + 1}'
        if not isinstance(e, dict):
            problems.append(f'{where}: not an object'); continue
        for k in REQUIRED:
            if not isinstance(e.get(k), str) or not e[k].strip():
                problems.append(f'{where}: missing "{k}"')
        if t.lower() in seen:
            problems.append(f'{where}: duplicate headword — merge the senses into one entry')
        seen.add(t.lower())

        if head(e.get('type')) not in TYPES:
            problems.append(f'{where}: type must open with one of {sorted(TYPES)}, got "{head(e.get("type"))}"')
        if head(e.get('position')) not in POSITIONS:
            problems.append(f'{where}: position must open with one of {sorted(POSITIONS)}, got "{head(e.get("position"))}"')
        comp = head(e.get('comparison'))
        if comp not in COMPARISONS:
            problems.append(f'{where}: comparison must open with one of {sorted(COMPARISONS)}, got "{comp}"')

        ipa = e.get('ipa') or ''
        if '/' in ipa:
            problems.append(f'{where}: ipa must not carry slashes')
        if 'ɒ' in ipa:
            problems.append(f'{where}: ipa uses ɒ — American English is ɑː')
        if re.search(r'e(?!ɪ)', ipa):
            problems.append(f'{where}: ipa has bare e — DRESS is ɛ, e only in eɪ')
        for d in ('ɪə', 'eə', 'ʊə'):
            if re.search(rf'(?<![aɔeoiu]){d}', ipa):
                problems.append(f'{where}: ipa has {d} — use ɪr/ɛr/ʊr')
        if not re.search(r'[A-Z]', e.get('respell') or ''):
            problems.append(f'{where}: respell has no CAPITAL stressed syllable')
        if not re.search(r'[а-яё]', (e.get('ru') or '').lower()):
            problems.append(f'{where}: ru has no Russian')

        for k, v in e.items():
            if isinstance(v, str) and v.count('*') % 2:
                problems.append(f'{where}: unbalanced asterisk in "{k}"')

        senses = e.get('senses')
        if not isinstance(senses, list) or not senses:
            problems.append(f'{where}: senses must be a non-empty list'); continue
        words = set(re.findall(r"[a-z']+", t.lower()))
        forms = set(spans(e.get('comparison') or ''))
        all_spans = []
        for n, s in enumerate(senses, 1):
            if not isinstance(s, dict):
                problems.append(f'{where}: sense {n} is not an object'); continue
            if not (s.get('gloss') or '').strip().endswith('.'):
                problems.append(f'{where}: sense {n} gloss must be a sentence ending in a period')
            ex = s.get('examples') or []
            want = (3, 3) if len(senses) == 1 else (2, 3)
            if not (want[0] <= len(ex) <= want[1]):
                problems.append(f'{where}: sense {n} has {len(ex)} examples, needs '
                                f'{want[0]}' + ('' if want[0] == want[1] else f'-{want[1]}'))
            for x in ex:
                if not isinstance(x, str):
                    problems.append(f'{where}: sense {n} has a non-string example'); continue
                if '**' in x:
                    problems.append(f'{where}: bold inside an example: {x[:50]}')
                if x.count('*') % 2:
                    problems.append(f'{where}: unbalanced asterisk: {x[:50]}')
                sp = spans(x)
                all_spans += sp
                if not any(words & set(re.findall(r"[a-z']+", s_)) or s_ in forms for s_ in sp):
                    problems.append(f'{where}: headword not asterisked in: {x[:60]}')
        if comp in WITH_FORMS:
            if not forms:
                problems.append(f'{where}: comparison "{comp}" must list the forms, e.g. -er/-est — *bigger*, *biggest*')
            elif not any(s_ in forms or any(f in s_ for f in forms) for s_ in all_spans):
                problems.append(f'{where}: no example uses a comparative or superlative ({", ".join(sorted(forms))})')
    return problems


if __name__ == '__main__':
    path = sys.argv[1]
    try:
        data = json.load(open(path, encoding='utf-8'))
    except Exception as exc:
        sys.exit(f'BAD JSON: {exc}')
    problems = check(data)
    if problems:
        print(f'{len(problems)} problem(s) in {path}:')
        for p in problems:
            print('  ', p)
        sys.exit(1)
    print(f'OK — {len(data)} entries in {path}')
