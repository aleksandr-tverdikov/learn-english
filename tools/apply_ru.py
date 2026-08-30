#!/usr/bin/env python3
"""Inject the Russian gloss into each dictionary entry from the per-file translation JSON.

Translators write only `<catalog>/data/ru/<slug>.json`, a flat {headword: gloss} map.
This script writes the `**Русский:**` line into the markdown, immediately after the
Pronunciation line. It is idempotent: an existing line is replaced, never duplicated,
so it is safe to re-run after any translation pass.
"""
import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, plain
from catalogs import CATALOGS

RU_LINE = re.compile(r'^\*\*Русский:\*\*.*$')
PRON_LINE = re.compile(r'^\*\*Pronunciation:\*\*')


def apply_file(md_path, table):
    lines = open(md_path).read().split('\n')
    out, i, added, updated, missing = [], 0, 0, 0, []
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        m = re.match(r'^###\s+(.+?)\s*$', ln)
        if not m:
            i += 1
            continue
        term = plain(m.group(1))
        gloss = table.get(term) or table.get(term.lower())
        # copy the entry's label block, dropping any existing Русский line
        i += 1
        pron_at = None
        block = []
        while i < len(lines) and not lines[i].startswith('### '):
            if RU_LINE.match(lines[i]):
                i += 1
                continue
            block.append(lines[i])
            if pron_at is None and PRON_LINE.match(lines[i]):
                pron_at = len(block)
            i += 1
            if len(block) > 400:
                break
        if gloss:
            if pron_at is None:
                missing.append(term + ' (no Pronunciation line)')
            else:
                had = any(RU_LINE.match(l) for l in lines)
                block.insert(pron_at, f'**Русский:** {gloss}')
                added += 1
        else:
            missing.append(term)
        out.extend(block)
    open(md_path, 'w').write('\n'.join(out))
    return added, missing


if __name__ == '__main__':
    total_added, total_missing, files_done, files_absent = 0, [], 0, 0
    for cfg in CATALOGS:
        cat = os.path.join(ROOT, cfg['dir'])
        if not os.path.isdir(cat):
            continue
        for md in sorted(glob.glob(os.path.join(cat, '[0-9]*.md'))):
            slug = os.path.basename(md)[:-3]
            ru = os.path.join(cat, 'data', 'ru', slug + '.json')
            if not os.path.exists(ru):
                files_absent += 1
                continue
            try:
                table = json.load(open(ru))
            except Exception as e:
                print(f'  BAD JSON {ru}: {e}')
                continue
            table = {plain(k): v for k, v in table.items() if isinstance(v, str) and v.strip()}
            added, missing = apply_file(md, table)
            total_added += added
            total_missing.extend(f'{slug}: {t}' for t in missing)
            files_done += 1
    print(f'glossed {total_added} entries across {files_done} files '
          f'({files_absent} files have no translation yet)')
    if total_missing:
        print(f'entries still without a gloss: {len(total_missing)}')
        for t in total_missing[:10]:
            print('   ', t)
