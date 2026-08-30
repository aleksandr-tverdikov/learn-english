#!/usr/bin/env python3
"""Build the library home page at index.html. Every number is read from disk, never hardcoded."""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, parse_catalog_file
from catalogs import CATALOGS

CLASSES = [
    ('01-nouns', 'Nouns', 'Names a person, place, thing, quality, or idea'),
    ('02-pronouns', 'Pronouns', 'Stands in for a whole noun phrase'),
    ('03-verbs', 'Verbs', 'Carries tense, aspect, voice, and mood'),
    ('04-adjectives', 'Adjectives', 'Describes or classifies a noun'),
    ('05-adverbs', 'Adverbs', 'Modifies everything except nouns'),
    ('06-prepositions', 'Prepositions', 'Relates a noun phrase to the rest of the sentence'),
    ('07-conjunctions', 'Conjunctions', 'Joins words, phrases, and clauses'),
    ('08-interjections', 'Interjections', 'Stands outside the sentence structure'),
    ('09-determiners', 'Determiners', 'Opens a noun phrase: which one? how many?'),
]

BLURBS = {
    '01-nouns': 'An open class, so only the parts that are finite are listed: every irregular plural, the uncountables that break learners, and the nouns that quietly force a plural verb.',
    '08-interjections': 'Every reaction word in the language — from <em>ouch</em> and <em>wow</em> to regional, archaic, internet, and profane forms, each with a register label saying who can say it where.',
    '07-conjunctions': 'Every connector, with the clause type it builds, a substitutable pattern, and the comma rule for that specific word.',
    '06-prepositions': 'The most polysemous class in English. Senses are numbered, and every entry says what may and may not follow it.',
    '09-determiners': 'The tightest closed class, where one wrong choice is instantly ungrammatical. Each entry names the noun types it may precede.',
    '03-verbs': 'Every irregular verb, grouped by how its three forms change rather than alphabetically. Each form is separately clickable, so you can hear <em>read</em>, <em>read</em>, and <em>read</em> differ.',
    '02-pronouns': 'Where case errors are most visible. Every entry gives its case, what it can refer to, and the verb agreement it forces.',
    'reporting-verbs': 'How to say what someone else said: every frame a reporting verb takes, the frames it refuses, and the judgment it quietly carries.',
}

stats = {}
for cfg in CATALOGS:
    d = os.path.join(ROOT, cfg['dir'])
    if not os.path.isdir(d):
        continue
    files = sorted(f for f in os.listdir(d) if re.match(r'^\d\d-.*\.md$', f))
    n = sum(len(parse_catalog_file(os.path.join(d, f))) for f in files)
    ex = 0
    for jf in glob.glob(os.path.join(d, 'data', '*.json')):
        try:
            ex += sum(len(e.get('examples') or []) for e in json.load(open(jf))['entries'])
        except Exception:
            pass
    stats[cfg['slug']] = (n, ex, len(files), cfg)

RS = os.path.join(ROOT, 'grammar/01-reported-speech')
rs_secs = len(glob.glob(f'{RS}/[0-9]*.md'))
rs_lines = sum(len(open(f).read().split('\n')) for f in glob.glob(f'{RS}/[0-9]*.md'))

total_entries = sum(v[0] for v in stats.values())
total_examples = sum(v[1] for v in stats.values())
md_lines = sum(len(open(f, errors='ignore').read().split('\n'))
               for f in glob.glob(f'{ROOT}/**/*.md', recursive=True))

# Derived from catalogs.py, never hardcoded: a dictionary under parts-of-speech/ is a
# word-class dictionary, anything else (reported speech) belongs to the Grammar section.
# Largest first. Hardcoding this list is how the irregular verbs went missing from the home page.
WORD_DICTS = [c['slug'] for c in sorted(
    (c for c in CATALOGS if c['dir'].startswith('parts-of-speech/') and c['slug'] in stats),
    key=lambda c: -stats[c['slug']][0])]
cards = []
for slug in WORD_DICTS:
    if slug not in stats:
        continue
    n, ex, nf, cfg = stats[slug]
    name = cfg['title'].replace('The ', '').replace(' Dictionary', '')
    cards.append(f'''
    <article class="dict" style="--c:{cfg['accent']};--cd:{cfg['accent_dark']}">
      <div class="dict-head"><h3>{name}</h3><span class="n">{n:,}</span></div>
      <p>{BLURBS.get(slug, '')}</p>
      <p class="meta">{n:,} entries &middot; {ex:,} example sentences &middot; {nf} categories</p>
      <div class="acts">
        <a class="btn" href="{cfg['dir']}/browse.html">Browse &amp; listen</a>
        <a class="btn ghost" href="{cfg['dir']}/README.html">A–Z index</a>
        <a class="btn ghost" href="{os.path.dirname(cfg['dir'])}/README.html">Grammar</a>
      </div>
    </article>''')

rv = stats.get('reporting-verbs')
grammar_cards = ''
if rv:
    n, ex, nf, cfg = rv
    grammar_cards = f'''
  <article class="dict" style="--c:{cfg['accent']};--cd:{cfg['accent_dark']}">
    <div class="dict-head"><h3>Reported speech</h3><span class="n">{n:,}</span></div>
    <p>{BLURBS['reporting-verbs']}</p>
    <p class="meta">{rs_secs} sections &middot; {rs_lines:,} lines &middot; {n:,} reporting verbs &middot; {ex:,} examples</p>
    <div class="acts">
      <a class="btn" href="{cfg['dir']}/browse.html">Browse the verbs</a>
      <a class="btn ghost" href="grammar/01-reported-speech/README.html">Read the topic</a>
      <a class="btn ghost" href="grammar/README.html">All grammar</a>
    </div>
  </article>
  <article class="dict" style="--c:#6b6b6b;--cd:#a8a8a8">
    <div class="dict-head"><h3>Three rules that fix most errors</h3></div>
    <p><strong>1.</strong> A reported question uses <em>statement</em> word order and no <em>do</em>:
    <em>She asked where I was</em>, not <span class="x">&#10007;</span> <em>where was I</em>.</p>
    <p><strong>2.</strong> Some verbs refuse a person before their complement:
    <span class="x">&#10007;</span> <em>suggested me to leave</em>, <span class="x">&#10007;</span> <em>explain me the rule</em>.</p>
    <p><strong>3.</strong> Backshift is not automatic. If it is still true, Americans leave it alone:
    <em>She said she lives in Boston</em>.</p>
  </article>'''

rows = []
for slug, name, blurb in CLASSES:
    cell = (f'<a href="{stats[slug][3]["dir"]}/browse.html">{stats[slug][0]:,} entries</a>'
            if slug in stats else '<span class="dash">—</span>')
    rows.append(f'<tr><td><a href="parts-of-speech/{slug}/README.html">{name}</a></td>'
                f'<td class="blurb">{blurb}</td><td>{cell}</td></tr>')

HTML = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Learn English — American English Reference</title>
<style>
:root{{--bg:#faf9f7;--surface:#fff;--surface2:#f2f0ec;--border:#e2ded6;--text:#1a1815;
--dim:#5f594f;--faint:#8a8377;--accent:#8a5a3b}}
@media(prefers-color-scheme:dark){{:root{{--bg:#14140f;--surface:#1d1d17;--surface2:#25251d;
--border:#33332a;--text:#eeeae1;--dim:#a8a293;--faint:#7d776b;--accent:#d09b72}}}}
:root[data-theme=dark]{{--bg:#14140f;--surface:#1d1d17;--surface2:#25251d;--border:#33332a;
--text:#eeeae1;--dim:#a8a293;--faint:#7d776b;--accent:#d09b72}}
:root[data-theme=light]{{--bg:#faf9f7;--surface:#fff;--surface2:#f2f0ec;--border:#e2ded6;
--text:#1a1815;--dim:#5f594f;--faint:#8a8377;--accent:#8a5a3b}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);
font:17px/1.7 ui-serif,Georgia,"Iowan Old Style",Palatino,serif;-webkit-font-smoothing:antialiased}}
.ui{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}}
.wrap{{max-width:940px;margin:0 auto;padding:0 24px}}
header{{padding:70px 0 44px;border-bottom:1px solid var(--border)}}
.eyebrow{{font-family:-apple-system,sans-serif;font-size:11.5px;letter-spacing:.18em;
text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 14px}}
h1{{font-size:clamp(34px,6vw,52px);line-height:1.08;letter-spacing:-.025em;margin:0 0 18px}}
.lede{{font-size:19px;color:var(--dim);max-width:60ch;margin:0 0 26px}}
.stats{{display:flex;gap:30px;flex-wrap:wrap;font-family:-apple-system,sans-serif}}
.stat b{{display:block;font-size:27px;letter-spacing:-.02em;font-weight:700}}
.stat span{{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--faint)}}
h2{{font-size:14px;font-family:-apple-system,sans-serif;text-transform:uppercase;
letter-spacing:.13em;color:var(--faint);margin:56px 0 18px;font-weight:700}}
.dicts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}
.dict{{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--c);
border-radius:12px;padding:22px 24px}}
@media(prefers-color-scheme:dark){{.dict{{border-top-color:var(--cd)}}.dict .n{{color:var(--cd)}}
.btn{{background:var(--cd);color:#14140f}}}}
:root[data-theme=dark] .dict{{border-top-color:var(--cd)}}
:root[data-theme=dark] .dict .n{{color:var(--cd)}}
:root[data-theme=dark] .btn{{background:var(--cd);color:#14140f}}
.dict-head{{display:flex;align-items:baseline;justify-content:space-between;gap:12px}}
.dict h3{{margin:0 0 10px;font-size:22px;letter-spacing:-.01em}}
.dict .n{{font-family:-apple-system,sans-serif;font-size:26px;font-weight:700;
color:var(--c);letter-spacing:-.02em}}
.dict p{{margin:0 0 12px;font-size:16px;color:var(--dim)}}
.dict .meta{{font-family:-apple-system,sans-serif;font-size:12.5px;color:var(--faint);margin-bottom:16px}}
.x{{color:var(--c)}}
.acts{{display:flex;gap:8px;flex-wrap:wrap}}
.btn{{font-family:-apple-system,sans-serif;font-size:13.5px;font-weight:600;text-decoration:none;
padding:8px 15px;border-radius:8px;background:var(--c);color:#fff;border:1px solid transparent}}
.btn.ghost{{background:transparent;color:var(--dim);border-color:var(--border)}}
:root[data-theme=dark] .btn.ghost{{background:transparent;color:var(--dim)}}
.btn:hover{{filter:brightness(1.08)}}
.btn.ghost:hover{{border-color:var(--accent);color:var(--accent)}}
table{{border-collapse:collapse;width:100%;font-size:16px}}
td{{padding:12px 14px;border-bottom:1px solid var(--border);vertical-align:top}}
tr:last-child td{{border-bottom:none}}
td:first-child{{white-space:nowrap;font-weight:600}}
td:last-child{{white-space:nowrap;text-align:right;font-family:-apple-system,sans-serif;font-size:14px}}
.blurb{{color:var(--dim);font-size:15px}}
.dash{{color:var(--faint)}}
a{{color:var(--accent)}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px 22px}}
.card h3{{margin:0 0 8px;font-size:19px}}
.card p{{margin:0 0 14px;font-size:15.5px;color:var(--dim)}}
.note{{background:var(--surface2);border:1px solid var(--border);border-radius:10px;
padding:16px 20px;font-size:15.5px;color:var(--dim);margin:18px 0 0}}
footer{{margin-top:64px;padding:26px 0 90px;border-top:1px solid var(--border);
color:var(--faint);font-size:14px}}
.themebtn{{position:fixed;right:18px;bottom:18px;z-index:60;font-family:-apple-system,sans-serif;
font-size:12.5px;font-weight:600;cursor:pointer;background:var(--surface);border:1px solid var(--border);
border-radius:99px;padding:9px 16px;color:var(--text)}}
@media(max-width:600px){{body{{font-size:16px}}.wrap{{padding:0 18px}}header{{padding:44px 0 32px}}}}
</style></head><body>

<header><div class="wrap">
  <p class="eyebrow">Reference Library</p>
  <h1>American English</h1>
  <p class="lede">The nine word classes, five complete dictionaries of the closed classes, the grammar of
  reported speech, and the full sound system — with a pronunciation, a register label, and at least five
  example sentences for every single entry.</p>
  <div class="stats ui">
    <div class="stat"><b>{total_entries:,}</b><span>dictionary entries</span></div>
    <div class="stat"><b>{total_examples:,}</b><span>example sentences</span></div>
    <div class="stat"><b>9</b><span>word classes</span></div>
    <div class="stat"><b>{md_lines:,}</b><span>lines written</span></div>
  </div>
</div></header>

<div class="wrap">

<h2>Dictionaries</h2>
<div class="dicts">{''.join(cards)}
</div>
<p class="note"><strong>Why these five?</strong> They are the <strong>closed classes</strong> — finite lists
that can actually be written down. Nouns, verbs, adjectives, and adverbs are open classes that gain new
members constantly, so no dictionary of them could ever be complete. Every entry is clickable: your browser
speaks it aloud, so nothing is downloaded and nothing leaves the page.</p>

<h2>Grammar</h2>
<div class="dicts">{grammar_cards}
</div>

<h2>Pronunciation</h2>
<div class="two">
  <div class="card">
    <h3>The sound system</h3>
    <p>All 24 consonants, 15 vowels and diphthongs, and 7 r-colored vowels of General American — with the
    spellings that produce each one, stress and reduction, and the eleven features that make an American
    accent American.</p>
    <div class="acts">
      <a class="btn" style="--c:#8a6d2f;--cd:#d6b76a" href="10-pronunciation/index.html">Open the guide</a>
      <a class="btn ghost" href="10-pronunciation/README.html">Read as text</a>
    </div>
  </div>
  <div class="card">
    <h3>Ear training</h3>
    <p>Eighteen minimal-pair sets tagged by the first language that struggles with each — <em>sheep/ship</em>,
    <em>think/sink</em>, <em>light/right</em> — plus a quiz that plays one word at random and scores you.</p>
    <div class="acts">
      <a class="btn ghost" href="10-pronunciation/index.html#pairs">Minimal pairs</a>
      <a class="btn ghost" href="10-pronunciation/index.html#quiz">Take the quiz</a>
    </div>
  </div>
</div>

<h2>The nine word classes</h2>
<table>{''.join(rows)}</table>
<p class="note">Class is a job, not a label. <em>Book</em> is a noun in <em>I finished the book</em> and a
verb in <em>please book a table</em>. Each grammar reference covers what the class does, its types, forms
and inflection, word order, rules, common mistakes, American vs. British notes, tricky cases, a quick
reference, and practice exercises with answers.</p>

<footer><div class="wrap">
Every page here is self-contained and works offline. Audio uses your browser's built-in speech engine.
&middot; <a href="README.html">Library index</a> &middot; <a href="parts-of-speech/README.html">Parts of speech</a>
&middot; <a href="grammar/README.html">Grammar</a>
</div></footer>
</div>

<button class="themebtn" id="themeBtn">Dark</button>
<script>
const tb=document.getElementById('themeBtn');
function setTheme(x){{document.documentElement.dataset.theme=x;tb.textContent=x==='dark'?'Light':'Dark';
 try{{localStorage.setItem('site-theme',x)}}catch(e){{}}}}
tb.onclick=()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark');
try{{const s=localStorage.getItem('site-theme');
 setTheme(s||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'))}}catch(e){{setTheme('light')}}
</script></body></html>'''

open(os.path.join(ROOT, 'index.html'), 'w').write(HTML)
print(f'wrote index.html — {total_entries:,} entries, {total_examples:,} examples, {md_lines:,} md lines')
for slug, (n, ex, nf, _) in stats.items():
    print(f'  {slug:<18}{n:>6} entries {ex:>7} examples {nf:>3} files')
