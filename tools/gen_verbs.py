#!/usr/bin/env python3
"""Render core-verb entries from tuples, the way gen_core.py does for nouns.

A verb entry carries more than a noun entry does, because the forms are the whole
difficulty: a learner who knows `explain` still has to produce `explains`,
`explained` and `explaining`, and the spelling rules that govern them are where
regular verbs actually go wrong.
"""
import os


def render(term, ipa, respell, ru, third, past, participle, ing,
           transitivity, gloss, examples, contrast=None):
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
    out += ['', gloss, '']
    for i, ex in enumerate(examples, 1):
        out.append(f'{i}. {ex}')
    return '\n'.join(out)


def build(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← The grammar of verbs](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    body = '\n\n---\n\n'.join(render(*e) for e in entries)
    open(path, 'w').write('\n'.join(head) + body + '\n')
    print(f'{os.path.basename(path):<34}{len(entries):>5} entries')
