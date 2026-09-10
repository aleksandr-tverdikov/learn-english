#!/usr/bin/env python3
"""Emit a core-vocabulary catalog file from a compact entry list.

The noun catalog has two tiers. Groups 1-23 are the *grammar-bearing* nouns —
irregular plurals, uncountables, forced agreement — and each gets a full entry
with senses, contrast notes, and a dozen examples, because each has a story.

Groups 24+ are *core vocabulary*: frequent, well-behaved nouns that a learner
needs to look up but that carry no grammatical surprise. A regular countable
noun like `table` does not need four hundred words, so these get a lean entry:
pronunciation, Russian, plural, countability, a one-line gloss, three examples.

Writing those by hand is all markup and no content, so they are authored as
tuples and rendered here. That also makes malformed entries impossible.

    (term, ipa, respell, ru, plural, countability, gloss, [examples], contrast?)

`plural` may be '' for an uncountable noun; `contrast` is optional.
"""
import sys, os


def render(term, ipa, respell, ru, plural, count, gloss, examples, contrast=None,
           senses=None):
    """One entry. `senses` promotes it to the numbered-sense shape.

    A word written by more than one semantic field usually has more than one
    meaning — `alarm` is a feeling to the emotions writer and a device to the
    time writer, and both are right. Collapsing those to whichever was written
    first loses half the word, so a merged entry lists them as numbered senses,
    the same shape the hand-written grammar tier uses.
    """
    out = [f'### {term}', '']
    out.append(f'**Pronunciation:** /{ipa}/ &middot; *{respell}*')
    out.append(f'**Русский:** {ru}')
    if plural:
        out.append(f'**Plural:** *{plural}*')
    out.append(f'**Countability:** {count}')
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
        head = sg.rstrip('.')
        out.append(f'**{k}. {head}.**' + (f' ({sru})' if sru else ''))
        out.append('')
        for ex in sex:
            n += 1
            out.append(f'{n}. {ex}')
        out.append('')
    return '\n'.join(out).rstrip()


def build(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← The grammar of nouns](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    body = '\n\n---\n\n'.join(render(*e) for e in entries)
    open(path, 'w').write('\n'.join(head) + body + '\n')
    print(f'{os.path.basename(path):<32}{len(entries):>4} entries')
