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


def render(term, ipa, respell, ru, plural, count, gloss, examples, contrast=None):
    out = [f'### {term}', '']
    out.append(f'**Pronunciation:** /{ipa}/ &middot; *{respell}*')
    out.append(f'**Русский:** {ru}')
    if plural:
        out.append(f'**Plural:** *{plural}*')
    out.append(f'**Countability:** {count}')
    if contrast:
        out.append(f'**Contrast:** {contrast}')
    out += ['', gloss, '']
    for i, ex in enumerate(examples, 1):
        out.append(f'{i}. {ex}')
    return '\n'.join(out)


def build(path, title, blurb, lede, entries):
    head = [f'# {title}', '', f'> {blurb}', '',
            '[← The grammar of nouns](../README.md) &middot; [All groups](README.md)', '',
            lede, '', '---', '']
    body = '\n\n---\n\n'.join(render(*e) for e in entries)
    open(path, 'w').write('\n'.join(head) + body + '\n')
    print(f'{os.path.basename(path):<32}{len(entries):>4} entries')
