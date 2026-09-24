#!/usr/bin/env python3
"""Render adjective entries from the JSON shape described in tools/adjectives/FORMAT.md.

What a learner gets wrong with an adjective is rarely its meaning. It is where the word
may stand (*an asleep baby* is not English), how it compares (*more tired*, not
*tireder*), and which preposition it drags along (*afraid of*, *good at*). So those get
their own lines, and the first clause of type, position and comparison is what the
browser shows as a filter tag.
"""

LABELS = [('type', 'Type'), ('position', 'Position'), ('comparison', 'Comparison'),
          ('takes', 'Takes'), ('_patterns', 'Preposition patterns'), ('form', 'Form'),
          ('opposite', 'Opposite'), ('contrast', 'Contrast')]


def render(e):
    """One entry. A single sense renders as gloss + examples; several as numbered senses."""
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

    out += ['', f'{term[0].upper() + term[1:]} has {len(senses)} distinct senses.', '']
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
