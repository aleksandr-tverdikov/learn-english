#!/usr/bin/env python3
"""Shared parsing for the Learn English build pipeline.

The markdown is the single source of truth. Everything else — the JSON, the A-Z indexes,
the audio browsers, the HTML site — is generated from it.

Entry format the parsers expect:

    ### headword

    **Pronunciation:** /ipa/ &middot; *RESPELL* &middot; optional note
    **Type:** ... &middot; **Case:** ... &middot; **Register:** ...     <- extra labels may ride inline
    **Some Field:** ...
    **Another Field:** ...

    Intro prose.

    **1. A numbered sense.** Its explanation.

    1. Example sentence.
    2. Example sentence.

    > "Direct speech."  ->  Reported version.        <- optional transformation pairs

    **See also:** [x](#x)

An entry is recognized by having a **Pronunciation:** line within the first few lines of its
body — NOT by the bare `###`, because some files legitimately use `###` for prose sections.
"""
import html, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LABEL = re.compile(r"^\s*\*\*(?!\d)(.+?):\*\*\s*(.*)$")
EXAMPLE = re.compile(r'^\s*(\d+)\.\s+(.*)$')
# The head may itself contain italics — `**6. *can't* — impossibility.**` — so it cannot be
# matched with [^*]: that stops at the first asterisk and silently drops the sense.
SENSE = re.compile(r'^\s*\*\*(\d+)[.)]\s*((?:[^*]|\*[^*]+\*)*?)\*\*\s*(.*)$')
INLINE_LABEL = re.compile(r'\*\*([A-Za-z][A-Za-z /\'-]*):\*\*\s*'
                          r'(.*?)(?=\*\*[A-Za-z][A-Za-z /\'-]*:\*\*|$)')

SEP_TAIL = re.compile(r'\s*(?:&middot;|·)\s*$')

ENTITIES = ['&middot;', '&mdash;', '&ndash;', '&nbsp;', '&hellip;', '&amp;',
            '&larr;', '&rarr;', '&times;', '&#9656;', '&#10007;']


def esc(s):
    """Escape for HTML while preserving entities the source deliberately used."""
    holders = {}
    for i, e in enumerate(ENTITIES):
        if e in s:
            k = f'\x00{i}\x00'
            s = s.replace(e, k)
            holders[k] = e
    s = html.escape(s, quote=False)
    for k, v in holders.items():
        s = s.replace(k, v)
    return s


def emphasis(s):
    """Bold/italic, in the only order that survives all five nestings the corpus uses.

    Plain bold MUST convert before italic: once **x** is gone, a stray * cannot confuse
    the italic pass. Special-casing each nesting shape instead produces greedy patterns
    that silently swallow whole paragraphs.
    """
    s = re.sub(r'\*\*\*([^*]+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
    s = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*\*((?:[^*]|\*[^*]+\*)+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', s)
    return s


def md_inline(s, keep_links=False):
    """Markdown inline -> safe HTML."""
    codes = []
    s = re.sub(r'`([^`]+)`', lambda m: (codes.append(m.group(1)), f'\x01{len(codes)-1}\x01')[1], s)
    if not keep_links:
        s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    s = esc(s)
    s = emphasis(s)
    for i, c in enumerate(codes):
        s = s.replace(f'\x01{i}\x01', f'<code>{html.escape(c, quote=False)}</code>')
    return s


def plain(s):
    """Strip all markup down to readable text (for speech, search, and slugs)."""
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
    for e, r in [('&middot;', '·'), ('&mdash;', '—'), ('&ndash;', '–'),
                 ('&amp;', '&'), ('&nbsp;', ' '), ('&#10007;', '✗')]:
        s = s.replace(e, r)
    return re.sub(r'\s+', ' ', re.sub(r'[*_`]', '', s)).strip()


def slugify(t):
    """GitHub's rule: strip markup and punctuation, then EACH space becomes one hyphen.

    Runs of spaces are NOT collapsed — `as ... as` yields `as--as`. Collapsing them
    silently breaks every anchor into a heading that contains punctuation.
    """
    s = re.sub(r'<[^>]+>', '', t)
    s = re.sub(r'[*_`]', '', s).lower().strip()
    s = re.sub(r"[^\w\s-]", '', s)
    return s.replace(' ', '-')


def parse_entry_body(body):
    """-> (labels, intro, senses, loose_examples, quotes)"""
    labels, intro, senses, loose, quotes = {}, [], [], [], []
    cur, block = None, []

    def flush():
        nonlocal block
        if block:
            text = ' '.join(block).strip()
            block = []
            if text:
                (cur['body'] if cur else intro).append(text)

    for ln in body:
        m = LABEL.match(ln)
        if m:
            flush()
            key, val = plain(m.group(1)).lower().strip(), m.group(2).strip()
            # a label line may carry further labels inline: **Type:** x &middot; **Case:** y
            extra = list(INLINE_LABEL.finditer(val))
            if extra:
                val = val[:extra[0].start()]
                for e in extra:
                    labels[plain(e.group(1)).lower().strip()] = SEP_TAIL.sub('', e.group(2).strip()).strip()
            labels[key] = SEP_TAIL.sub('', val).strip()
            continue
        s = SENSE.match(ln)
        if s:
            flush()
            cur = {'n': s.group(1), 'head': plain(s.group(2)).rstrip('.'),
                   'body': [], 'examples': [], 'quotes': []}
            senses.append(cur)
            if s.group(3).strip():
                block.append(s.group(3).strip())
            continue
        e = EXAMPLE.match(ln)
        if e:
            flush()
            (cur['examples'] if cur else loose).append(e.group(2).strip())
            continue
        t = ln.strip()
        if not t:
            flush()
            continue
        if t.startswith('>'):
            q = t.lstrip('> ').strip()
            if q:
                (cur['quotes'] if cur else quotes).append(q)
            continue
        if re.match(r'^([-*+]\s|#{1,6}\s|\||<)', t):
            continue
        block.append(t)
    flush()
    return labels, intro, senses, loose, quotes


def parse_catalog_file(path):
    """Every entry in one catalog markdown file, with GitHub-correct anchors.

    Anchors are numbered across ALL `###` headings (GitHub dedupes over all of them),
    but only entry headings are returned — otherwise every anchor after a prose
    section would be silently off by one.
    """
    lines = open(path).read().split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('### ')]
    # An entry body ends at the next heading of ANY level. Stopping only at the next
    # `### ` sweeps the prose under an intervening `## ` section heading into the
    # previous entry, so the last entry of each section absorbs the next section's lede
    # — and the last entry of the file absorbs every closing note after it.
    stops = [i for i, l in enumerate(lines) if re.match(r'^#{1,6} ', l)]
    seen, out = defaultdict(int), []
    for j, i in enumerate(idx):
        end = next((s for s in stops if s > i), len(lines))
        term = plain(lines[i][4:])
        body = lines[i + 1:end]
        b = slugify(term)
        n = seen[b]
        seen[b] += 1
        anchor = b if n == 0 else f'{b}-{n}'
        if not any('**Pronunciation:**' in l for l in body[:8]):
            continue
        labels, intro, senses, loose, quotes = parse_entry_body(body)

        pron = labels.get('pronunciation', '')
        parts = re.split(r'&middot;|·', pron)
        respell, note = '', ''
        if len(parts) > 1:
            # documented shape: /ipa/ &middot; *RESPELL* &middot; note. The respelling is
            # chunk 2 alone; anything after an em dash inside it is already note text.
            bits = re.split(r'&mdash;|—', parts[1], maxsplit=1)
            respell = plain(bits[0])
            tail = ([bits[1]] if len(bits) > 1 else []) + list(parts[2:])
            note = ' &middot; '.join(t.strip() for t in tail if t.strip())
        if len(respell) > 60:          # a run-on "respelling" is really a note
            note, respell = respell + ((' — ' + note) if note else ''), ''
        labels['_pron_note'] = note

        out.append({
            'term': term, 'anchor': anchor,
            'ipa': plain(parts[0]) if parts else '',
            'respell': respell,
            'labels': labels,
            'intro': intro, 'senses': senses, 'loose': loose, 'quotes': quotes,
        })
    return out


def title_of(md, fallback=''):
    m = re.search(r'^#\s+(.+)$', md, re.M)
    return plain(m.group(1)) if m else fallback


def blurb_of(md):
    m = re.search(r'^>\s*(.+)$', md, re.M)
    return plain(m.group(1)) if m else ''
