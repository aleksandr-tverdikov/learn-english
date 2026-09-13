#!/usr/bin/env python3
"""Render core-verb entries from tuples, the way gen_core.py does for nouns.

A verb entry carries more than a noun entry does, because the forms are the whole
difficulty: a learner who knows `explain` still has to produce `explains`,
`explained` and `explaining`, and the spelling rules that govern them are where
regular verbs actually go wrong.
"""
import os


def render(term, ipa, respell, ru, third, past, participle, ing,
           transitivity, gloss, examples, contrast=None, senses=None):
    """One verb entry. `senses` promotes it to the numbered-sense shape.

    Verbs are more polysemous than nouns, not less: *run* a race, *run* a company,
    *run* a program, *run* for office. A regular verb written by a single semantic
    field gets only that field's meaning, so this renders the rest alongside it,
    in the same shape the irregular tier already uses.
    """
    out = [f'### {term}', '']
    out.append(f'**Pronunciation:** /{ipa}/ &middot; *{respell}*')
    out.append(f'**Русский:** {ru}')
    out.append(f'**Forms:** *{term}* &middot; *{past}* &middot; *{participle}*')
    out.append(f'**Third person:** *{third}* &middot; **-ing form:** *{ing}*')
    out.append('**Verb class:** regular')
    if transitivity:
        out.append(f'**Transitivity:** {transitivity}')
    if contrast:
        out.append(f'**Contrast:** {contrast}')
    if not senses:
        out += ['', gloss, '']
        for i, ex in enumerate(examples, 1):
            out.append(f'{i}. {ex}')
        return '\n'.join(out)

    out += ['', f'{term.capitalize()} has {len(senses)} distinct senses.', '']
    n = 0
    for k, (sg, sru, sex) in enumerate(senses, 1):
        out.append(f'**{k}. {sg.rstrip(".")}.**' + (f' ({sru})' if sru else ''))
        out.append('')
        for ex in sex:
            n += 1
            out.append(f'{n}. {ex}')
        out.append('')
    return '\n'.join(out).rstrip()


def build(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← The grammar of verbs](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    body = '\n\n---\n\n'.join(render(*e) for e in entries)
    open(path, 'w').write('\n'.join(head) + body + '\n')
    print(f'{os.path.basename(path):<34}{len(entries):>5} entries')
