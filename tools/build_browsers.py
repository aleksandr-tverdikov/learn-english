#!/usr/bin/env python3
"""Build the searchable audio browser and the A-Z index for every dictionary.

Reads the markdown, writes:
    <catalog>/browse.html   the searchable browser (all entries embedded)
    <catalog>/README.md     the A-Z index
    <catalog>/data/*.json   the entries, kept in sync with the markdown
"""
import json, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import (ROOT, esc, md_inline, plain, slugify, parse_catalog_file, title_of, blurb_of)
from catalogs import CATALOGS

TEMPLATE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'browser_template.html')).read()



FORM_RE = re.compile(r'\*([^*]+)\*\s*(/[^/]*/)?')


def forms_of(raw):
    """`*abide* /əˈbaɪd/ &middot; *abode* /əˈboʊd/` -> [{w, ipa}, ...]

    Each form gets its own entry so the browser can speak it. Without this the past
    and participle are unspoken text — the opposite of what an irregular-verb table needs.
    """
    if not raw.strip():
        return []
    out = []
    for chunk in re.split(r'&middot;|·', raw):
        # a slot may hold more than one form: "*was* /wʌz/, *were* /wɝ/"
        for m in FORM_RE.finditer(chunk):
            w = plain(m.group(1))
            if w and not w.startswith('('):
                out.append({'w': w, 'ipa': plain(m.group(2) or '')})
    return out if len(out) > 1 else []


RARE_RE = re.compile(r'\b(archaic|obsolete|literary|biblical|poetic|dated|rare|nonstandard|'
                     r'non-standard|dialect\w*|regional|british)\b', re.I)


def tier_of(register, term=''):
    """'core' = ordinary modern American; 'rare' = archaic, literary, regional, or British.

    Classified from the FIRST clause of the Register label only. Later clauses are usually
    contrastive ("neutral; archaic in the legal sense") and would otherwise set aside an
    entry that is perfectly ordinary in its main use.
    """
    # split on the em dash too: registers often read 'formal and careful — <long gloss>',
    # and scanning the gloss sets aside entries whose actual register is ordinary.
    first = re.split(r'[;(]|—|--', plain(register or ''))[0]
    return 'rare' if RARE_RE.search(first) else 'core'


XREF = re.compile(r'\[([^\]]+)\]\(([0-9]{2}-[a-z0-9-]+)\.md#([^)]+)\)')


def as_inpage_links(raw):
    """Turn `[run across](19-phrasal-m-r.md#run-across)` into an in-page jump.

    Every entry in a browser lives on one page with id `e-<file>-<anchor>`, so a cross-file
    markdown link would go nowhere. md_inline() strips links entirely, which for this field
    would throw away the only useful thing in it.
    """
    def one(m):
        return f'<a class="xref" href="#e-{m.group(2)}-{m.group(3)}">{esc(m.group(1))}</a>'
    return XREF.sub(one, raw.replace('&middot;', '·'))


def _head(v):
    """the leading clause of a field, before any dash or parenthetical"""
    v = plain(v or '')
    v = re.split(r'[—(;,]|--| - ', v)[0]
    return v.strip().strip('.').lower()


def verb_tags(labels):
    """Short badges for the collapsed row: the classification without the prose.

    Each field opens with its verdict and then explains it. The verdict is what you want
    while scanning a list; the explanation is what you want once an entry is open.
    """
    tags = []
    vt = _head(labels.get('verb type'))
    for k in ('action', 'stative', 'linking', 'auxiliary', 'modal'):
        if k in vt:
            tags.append(k)
            break
    tr = _head(labels.get('transitivity')) or _head(labels.get('transitive'))
    if tr:
        if tr.startswith('both') or tr.startswith('either'):
            tags.append('trans + intrans')
        elif 'ditransitive' in tr:
            tags.append('ditransitive')
        elif tr.startswith('intransitive') or tr in ('no', 'none'):
            tags.append('intransitive')
        elif tr.startswith('transitive') or tr.startswith('yes'):
            tags.append('transitive')
    pv = _head(labels.get('passive'))
    if pv.startswith('yes'):
        tags.append('passive ✓')
    elif pv.startswith('no'):
        tags.append('no passive')
    elif pv.startswith('restricted'):
        tags.append('passive limited')
    return tags


# order matters: strip the trailing qualifier first, or 'plural countable nouns only'
# keeps its 'nouns' and collides with the already-trimmed 'plural countable'
TRIM = [(r'\s+only$', ''), (r'\s*\bclause of\b\s*', ': '), (r'\bpronouns?$', ''),
        (r'\bnouns?$', ''), (r'\bdeterminers?$', ''), (r'\bverbs?$', ''),
        (r'^a\s+', ''), (r'^the\s+', '')]


def generic_tags(labels, fields, common):
    """Short badges from the leading clause of each configured field.

    Two guards. A clause longer than 30 characters is prose, not a label, so it is left
    for the expanded entry. A value carried by almost every entry in the dictionary
    ('reporting verb' on all 313) says nothing and is dropped.
    """
    out = []
    for key in fields:
        h = _head(labels.get(key))
        if not h or h in ('none', 'n/a'):
            continue
        # test the raw head against the near-universal set: `common` is built from raw
        # heads, so comparing the trimmed form silently never matches
        if (key, h) in common:
            continue
        for pat, rep in TRIM:
            h = re.sub(pat, rep, h).strip()
        h = re.sub(r'\s{2,}', ' ', h).strip(' :')
        if not h or len(h) > 30:
            continue
        if h not in out:
            out.append(h)
    return out


def common_values(entries_labels, fields, n):
    """values so widespread they carry no information"""
    from collections import Counter
    c = Counter()
    for labels in entries_labels:
        for key in fields:
            h = _head(labels.get(key))
            if h:
                c[(key, h)] += 1
    return {k for k, v in c.items() if v > 0.85 * n}


FRAMES = [(r'\bsb\b[^.]{0,12}\bto[- ]inf|someone to do|\bobject \+ to\b', 'sb + to-inf'),
          (r'that[- ]clause', 'that-clause'),
          (r'wh[- ]clause', 'wh-clause'),
          (r'\+\s*\*?\*?-?ing|gerund', '-ing'),
          # only the explicit term: a bare '+ to' also appears in frames like
          # 'suggest + noun phrase + to + sb', and tagging suggest as taking a
          # to-infinitive inverts the one fact that entry exists to teach
          (r'to[- ]infinitive', 'to-inf'),
          (r'direct (?:quotation|speech)', 'direct quote'),
          (r'noun phrase', 'noun phrase')]


def pattern_tags(labels):
    """Which complement frames a reporting verb takes.

    Its `type` is 'reporting verb' on nearly every entry and says nothing. What separates
    these verbs is the frames they accept — and refuse, which is the whole point of the file.
    """
    raw = plain(labels.get('patterns') or labels.get('pattern') or '').lower()
    out = [name for pat, name in FRAMES if re.search(pat, raw)]
    if plain(labels.get('never') or '').strip():
        out.append('has restriction')
    return out[:5]

def build(cfg):
    cat_dir = os.path.join(ROOT, cfg['dir'])
    files = sorted(f for f in os.listdir(cat_dir) if re.match(r'^\d\d-.*\.md$', f))
    cats, entries = [], []
    tag_fields = cfg.get('tag_fields') or []
    all_labels = [e['labels'] for f in files for e in parse_catalog_file(os.path.join(cat_dir, f))]
    common = common_values(all_labels, tag_fields, len(all_labels)) if tag_fields else set()

    for fn in files:
        path = os.path.join(cat_dir, fn)
        md = open(path).read()
        slug = fn[:-3]
        got = parse_catalog_file(path)

        for e in got:
            labels = e['labels']
            fields = []
            note = labels.get('_pron_note', '')
            if note.strip():
                fields.append(['On the pronunciation', md_inline(note)])
            for key, disp in cfg['fields']:
                v = labels.get(key, '')
                if v.strip():
                    fields.append([disp, as_inpage_links(v) if key == 'phrasal verbs' else md_inline(v)])
            entries.append({
                't': e['term'], 'a': e['anchor'], 'c': slug,
                'i': e['ipa'], 'r': e['respell'],
                'g': plain(labels.get('register', '')),
                'ru': plain(labels.get('русский', '')),
                'tier': tier_of(labels.get('register', ''), e['term']),
                'd': 1 if slug.startswith(cfg.get('derived_prefixes', ())) else 0,
                'tg': verb_tags(labels) if cfg['slug'] == '03-verbs'
                      else pattern_tags(labels) if cfg['slug'] == 'reporting-verbs'
                      else generic_tags(labels, tag_fields, common),
                # the three verb forms, split out so each can be spoken on its own
                'fm': forms_of(labels.get('forms', '')),
                'intro': [md_inline(p) for p in e['intro']],
                'q': [md_inline(q) for q in e['quotes']],
                'x': [md_inline(x) for x in e['loose']],
                'xp': [plain(x) for x in e['loose']],
                'senses': [{'n': s['n'], 'h': md_inline(s['head']),
                            'b': [md_inline(p) for p in s['body']],
                            'q': [md_inline(q) for q in s.get('quotes', [])],
                            'x': [md_inline(x) for x in s['examples']],
                            'xp': [plain(x) for x in s['examples']]} for s in e['senses']],
                'f': fields,
            })
        cats.append({'slug': slug, 'title': title_of(md, slug), 'n': len(got),
                     'blurb': blurb_of(md)})

        # keep the JSON in sync with the markdown
        data = {'category': title_of(md, slug), 'slug': slug, 'entries': []}
        for e in got:
            lab = e['labels']
            rec = {'term': e['term'], 'ipa': e['ipa'], 'respell': e['respell'],
                   'meaning': plain(' '.join(e['intro'])),
                   'examples': [plain(x) for x in e['loose']] +
                               [plain(x) for s in e['senses'] for x in s['examples']],
                   'senses': [{'n': s['n'], 'head': s['head'],
                               'body': [plain(p) for p in s['body']],
                               'examples': [plain(x) for x in s['examples']]} for s in e['senses']]}
            if lab.get('_pron_note', '').strip():
                rec['pronunciation note'] = plain(lab['_pron_note'])
            for k, v in lab.items():
                if not k.startswith('_') and k != 'pronunciation':
                    rec[k] = plain(v)
            data['entries'].append(rec)
        os.makedirs(os.path.join(cat_dir, 'data'), exist_ok=True)
        json.dump(data, open(os.path.join(cat_dir, 'data', slug + '.json'), 'w'),
                  ensure_ascii=False, indent=2)

    total = len(entries)

    # ---- browser ----
    blob = json.dumps({'cats': [{k: c[k] for k in ('slug', 'title', 'n')} for c in cats],
                       'entries': entries}, ensure_ascii=False,
                      separators=(',', ':')).replace('</', '<\\/')
    out = (TEMPLATE.replace('__TITLE__', cfg['title'])
                   .replace('__EYEBROW__', cfg['eyebrow'])
                   .replace('__LEDE__', cfg['lede'])
                   .replace('__ACCENT__', cfg['accent'])
                   .replace('__ACCENT_DARK__', cfg['accent_dark'])
                   .replace('__THEMEKEY__', cfg['slug'])
                   .replace('__TOTAL__', f'{total:,}')
                   .replace('__DATA__', blob))
    open(os.path.join(cat_dir, 'browse.html'), 'w').write(out)

    # ---- A-Z index ----
    az = defaultdict(list)
    for e in entries:
        k = e['t'][0].upper() if e['t'][:1].isalpha() else '#'
        az[k].append((e['t'].lower(), e['t'], f"{e['c']}.md#{e['a']}"))
    letters = sorted([k for k in az if k != '#']) + (['#'] if '#' in az else [])

    o = [f"# {cfg['title']}\n",
         f"> **{total} entries** across {len(cats)} categories.\n",
         f"**[Open the audio browser](browse.html)** to search all {total} and hear any of them spoken.\n",
         '---\n', '## Categories\n', '| # | Category | What it covers | Entries |', '|---|---|---|---|']
    for i, c in enumerate(cats, 1):
        o.append(f"| {i} | [{c['title']}]({c['slug']}.md) | {c['blurb']} | {c['n']} |")
    o.append(f"| | **Total** | | **{total}** |\n")
    o.append('## Fields in each entry\n')
    o.append('| Field | What it tells you |')
    o.append('|---|---|')
    o.append('| Pronunciation | IPA, a stress-marked respelling, and the weak form where one exists |')
    for _, disp in cfg['fields']:
        o.append(f"| {disp} | |")
    o.append('')
    o.append('---\n')
    o.append(f'## A–Z index\n\nAll {total} headwords.\n')
    for L in letters:
        o.append(f'### {L}\n')
        o.append(' &middot; '.join(f'[{t}]({lnk})' for _, t, lnk in sorted(set(az[L]))))
        o.append('')
    open(os.path.join(cat_dir, 'README.md'), 'w').write('\n'.join(o) + '\n')

    n_sense = sum(1 for e in entries if e['senses'])
    n_ex = sum(len(e['x']) + sum(len(s['x']) for s in e['senses']) for e in entries)
    return total, n_sense, n_ex, len(out)


if __name__ == '__main__':
    only = sys.argv[1:] or None
    for cfg in CATALOGS:
        if only and cfg['slug'] not in only:
            continue
        if not os.path.isdir(os.path.join(ROOT, cfg['dir'])):
            print(f"{cfg['slug']:<18} SKIPPED (no directory)")
            continue
        total, ns, nx, size = build(cfg)
        print(f"{cfg['slug']:<18}{total:>6} entries {ns:>5} with senses {nx:>7} examples  {size/1e6:.2f} MB")
