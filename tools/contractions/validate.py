#!/usr/bin/env python3
"""Check one contraction JSON file against tools/contractions/FORMAT.md."""
import json, re, sys

TYPES = {'be', 'have', 'had', 'will', 'would', 'negative', 'modal', 'informal', 'dialect',
         # frozen forms whose parts no longer work as words: let's (= us), o'clock, ma'am
         'fixed'}
REGISTERS = {'standard', 'informal', 'nonstandard', 'regional', 'dated'}
REQUIRED = ('term', 'ipa', 'respell', 'ru', 'expands', 'type', 'register')


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
        if head(e.get('register')) not in REGISTERS:
            problems.append(f'{where}: register must open with one of {sorted(REGISTERS)}, got "{head(e.get("register"))}"')
        if not spans(e.get('expands') or ''):
            problems.append(f'{where}: expands must show the full form in asterisks, e.g. *will not*')

        ipa = e.get('ipa') or ''
        if '/' in ipa:
            problems.append(f'{where}: ipa must not carry slashes')
        if 'ɒ' in ipa:
            problems.append(f'{where}: ipa uses ɒ — American English is ɑː')
        if re.search(r'e(?!ɪ)', ipa):
            problems.append(f'{where}: ipa has bare e — DRESS is ɛ, e only in eɪ')
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
        if len(senses) > 1 and not (e.get('ambiguity') or '').strip():
            problems.append(f'{where}: more than one expansion, so "ambiguity" is required')
        core = t.lower().lstrip("'").replace("'", '')
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
                if not any(core in s_.replace("'", '') for s_ in spans(x)):
                    problems.append(f'{where}: headword not asterisked in: {x[:60]}')
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
