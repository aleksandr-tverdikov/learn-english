#!/usr/bin/env python3
"""Rewrite each verb entry's body from its numbered-sense JSON.

Translators/lexicographers write only `<catalog>/data/senses/<slug>.json`:

    {"abide": {"gloss": "To put up with, or to dwell.",
               "senses": [{"head": "Tolerate, put up with",
                           "ru": "терпеть, выносить",
                           "body": "Usually negative — cannot abide.",
                           "examples": ["I cannot abide people who talk.", "..."]}]}}

This script replaces everything between an entry's label block and its `**See also:**`
line with the rendered senses, numbering examples continuously so the shared parser
attaches each one to its own sense. It never touches the labels (Pronunciation, Forms,
Русский, Pattern...), and it is idempotent — rerunning regenerates the same body.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, plain

LABEL = re.compile(r'^\*\*(?!\d)[^*\n]+?:\*\*')
SEE_ALSO = re.compile(r'^\*\*See also:\*\*')


def render(rec):
    gloss = (rec.get('gloss') or '').strip()
    senses = rec.get('senses') or []
    out = []
    if gloss:
        out += ['', gloss]
    n = 1
    for i, s in enumerate(senses, 1):
        head = (s.get('head') or '').strip().rstrip('.')
        body = (s.get('body') or '').strip()
        ru = (s.get('ru') or '').strip()
        line = f'**{i}. {head}.**'
        if body:
            line += ' ' + body
        if ru:
            line += f' ({ru})'
        out += ['', line, '']
        for ex in s.get('examples') or []:
            ex = ex.strip()
            if ex:
                out.append(f'{n}. {ex}')
                n += 1
    return out, n - 1


def apply_file(md_path, table):
    lines = open(md_path).read().split('\n')
    out, i, done, untouched = [], 0, 0, 0
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        m = re.match(r'^###\s+(.+?)\s*$', ln)
        if not m:
            i += 1
            continue
        term = plain(m.group(1))
        rec = table.get(term) or table.get(term.lower())
        i += 1
        # Copy the label block verbatim. Blank lines count as part of it — the entry opens
        # with one, and treating that as the end of the labels drops Pronunciation, Forms
        # and Русский into the region this script replaces.
        while i < len(lines):
            l = lines[i]
            if SEE_ALSO.match(l) or l.startswith('### '):
                break
            if l.strip() and not LABEL.match(l):
                break
            out.append(l); i += 1
        while out and not out[-1].strip():   # drop trailing blanks; render() re-adds one
            out.pop()
        # find where this entry ends: its See also line, or the next heading
        j = i
        while j < len(lines) and not lines[j].startswith('### ') and not SEE_ALSO.match(lines[j]):
            j += 1
        if rec:
            body, _ = render(rec)
            out.extend(body)
            out.append('')
            done += 1
        else:
            out.extend(lines[i:j])
            untouched += 1
        i = j
    open(md_path, 'w').write('\n'.join(out))
    return done, untouched


if __name__ == '__main__':
    targets = sys.argv[1:] or ['parts-of-speech/03-verbs/catalog']
    tot_done = tot_skip = files = 0
    for cat in targets:
        cat = os.path.join(ROOT, cat)
        for md in sorted(glob.glob(os.path.join(cat, '[0-9]*.md'))):
            slug = os.path.basename(md)[:-3]
            src = os.path.join(cat, 'data', 'senses', slug + '.json')
            if not os.path.exists(src):
                continue
            try:
                table = json.load(open(src))
            except Exception as e:
                print(f'  BAD JSON {src}: {e}')
                continue
            table = {plain(k): v for k, v in table.items() if isinstance(v, dict)}
            d, u = apply_file(md, table)
            tot_done += d; tot_skip += u; files += 1
            print(f'  {slug:<38}{d:>4} rewritten {u:>4} left alone')
    print(f'\nrewrote {tot_done} entry bodies across {files} files ({tot_skip} had no sense data)')
