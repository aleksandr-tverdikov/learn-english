#!/usr/bin/env python3
"""Render contraction entries from the JSON shape in tools/contractions/FORMAT.md.

A contraction entry answers three questions a learner actually has: what it is short
for, whether the written form is ambiguous (*'s* is *is* or *has*; *'d* is *would* or
*had*), and whether it may be written down at all.
"""

LABELS = [('expands', 'Expands to'), ('type', 'Type'), ('register', 'Register'),
          ('ambiguity', 'Ambiguity'), ('question', 'Question form'), ('contrast', 'Contrast')]


def render(e):
    term = e['term']
    out = [f'### {term}', '']
    out.append(f"**Pronunciation:** /{e['ipa'].strip('/')}/ &middot; *{e['respell']}*")
    out.append(f"**Русский:** {e['ru']}")
    for key, label in LABELS:
        if (e.get(key) or '').strip():
            out.append(f'**{label}:** {e[key].strip()}')

    senses = e['senses']
    if len(senses) == 1:
        out += ['', senses[0]['gloss'].strip(), '']
        for i, ex in enumerate(senses[0]['examples'], 1):
            out.append(f'{i}. {ex}')
        return '\n'.join(out)

    out += ['', f'{term} stands for {len(senses)} different things.', '']
    n = 0
    for k, s in enumerate(senses, 1):
        head = s['gloss'].strip().rstrip('.')
        ru = (s.get('ru') or '').strip()
        out.append(f'**{k}. {head}.**' + (f' ({ru})' if ru else ''))
        out.append('')
        for ex in s['examples']:
            n += 1
            out.append(f'{n}. {ex}')
        out.append('')
    return '\n'.join(out).rstrip()
