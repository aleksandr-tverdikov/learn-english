#!/usr/bin/env python3
"""Render every Markdown file in the library to a styled, self-contained HTML page.

Links between .md files are rewritten to .html. Headings get GitHub-compatible ids so
that anchors written for GitHub keep working here.
"""
import html, os, re, sys, posixpath
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ROOT, esc, emphasis, plain, slugify, INLINE_LABEL, SEP_TAIL


def inline(s):
    codes = []
    s = re.sub(r'`([^`]+)`', lambda m: (codes.append(m.group(1)), f'\x01{len(codes)-1}\x01')[1], s)
    s = esc(s)

    def link(m):
        text, href = m.group(1), m.group(2)
        anchor = ''
        if '#' in href:
            href, anchor = href.split('#', 1)
            anchor = '#' + anchor
        if href.endswith('.md'):
            href = href[:-3] + '.html'
        return f'<a href="{html.escape(href + anchor, quote=True)}">{text}</a>'
    s = re.sub(r'\[([^\]]*)\]\(([^)\s]*)\)', link, s)
    s = emphasis(s)
    for i, c in enumerate(codes):
        s = s.replace(f'\x01{i}\x01', f'<code>{html.escape(c, quote=False)}</code>')
    return s


# `**Label:** value` — the field lines every dictionary entry is built from.
# The (?!\d) guard keeps numbered senses (**1. The core use.**) out of it.
FIELD_LINE = re.compile(r'^\*\*(?!\d)([^*\n]+?):\*\*\s*(.*)$')


def convert(md):
    lines = md.split('\n')
    out, i, toc = [], 0, []
    seen = defaultdict(int)

    def hid(text):
        b = slugify(text)
        n = seen[b]
        seen[b] += 1
        return b if n == 0 else f'{b}-{n}'

    while i < len(lines):
        ln = lines[i]

        if ln.startswith('```'):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith('```'):
                buf.append(lines[i]); i += 1
            i += 1
            out.append('<pre><code>' + html.escape('\n'.join(buf), quote=False) + '</code></pre>')
            continue

        if re.match(r'^\s*</?(details|summary|div|br|hr)\b', ln, re.I):
            out.append(ln); i += 1; continue

        if not ln.strip():
            i += 1; continue

        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            lvl, text = len(m.group(1)), m.group(2).strip()
            anchor = hid(text)
            if lvl == 2:
                toc.append((plain(text), anchor))
            out.append(f'<h{lvl} id="{anchor}">{inline(text)}'
                       f'<a class="hash" href="#{anchor}" aria-label="link">#</a></h{lvl}>')
            i += 1; continue

        if re.match(r'^(---+|___+|\*\*\*+)\s*$', ln):
            out.append('<hr>'); i += 1; continue

        if ln.lstrip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            def cells(r):
                r = r.strip()
                if r.startswith('|'): r = r[1:]
                if r.endswith('|'): r = r[:-1]
                return [c.strip() for c in re.split(r'(?<!\\)\|', r)]
            head = cells(ln)
            aligns = ['center' if c.startswith(':') and c.endswith(':')
                      else 'right' if c.endswith(':') else 'left' for c in cells(lines[i + 1])]
            i += 2
            body = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                body.append(cells(lines[i])); i += 1
            t = ['<div class="tw"><table><thead><tr>']
            for j, c in enumerate(head):
                t.append(f'<th style="text-align:{aligns[j] if j < len(aligns) else "left"}">{inline(c)}</th>')
            t.append('</tr></thead><tbody>')
            for row in body:
                t.append('<tr>')
                for j, c in enumerate(row):
                    t.append(f'<td style="text-align:{aligns[j] if j < len(aligns) else "left"}">{inline(c)}</td>')
                t.append('</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t)); continue

        if ln.lstrip().startswith('>'):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append('<blockquote>' + convert('\n'.join(buf))[0] + '</blockquote>')
            continue

        m = re.match(r'^(\s*)(\d+)[.)]\s+(.*)$', ln)
        if m:
            start = m.group(2)
            items = []
            while i < len(lines):
                mm = re.match(r'^(\s*)(\d+)[.)]\s+(.*)$', lines[i])
                if not mm: break
                items.append(inline(mm.group(3))); i += 1
            attr = f' start="{start}"' if start != '1' else ''
            out.append(f'<ol{attr}>' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>')
            continue

        if re.match(r'^(\s*)[-*+]\s+', ln):
            items = []
            while i < len(lines):
                mm = re.match(r'^(\s*)[-*+]\s+(.*)$', lines[i])
                if not mm: break
                items.append((len(mm.group(1)), inline(mm.group(2)))); i += 1
            buf, depth = ['<ul>'], 0
            for ind, txt in items:
                d = 1 if ind >= 2 else 0
                if d > depth: buf.append('<ul>')
                elif d < depth: buf.append('</ul>')
                depth = d
                buf.append(f'<li>{txt}</li>')
            buf.append('</ul>' * (depth + 1))
            out.append(''.join(buf)); continue

        # A run of `**Label:** value` lines is a field block, not a paragraph. Merging them
        # into one <p> — which is what plain Markdown does, here and on GitHub — produces the
        # unreadable wall of text that dictionary entries are made almost entirely of.
        if FIELD_LINE.match(ln):
            rows = []
            while i < len(lines) and FIELD_LINE.match(lines[i]):
                m = FIELD_LINE.match(lines[i])
                k, v = m.group(1).strip(), m.group(2).strip()
                # one line may carry several labels: **Type:** x &middot; **Case:** y &middot; **Register:** z
                extra = list(INLINE_LABEL.finditer(v))
                if extra:
                    rows.append((k, SEP_TAIL.sub('', v[:extra[0].start()]).strip()))
                    for e in extra:
                        rows.append((e.group(1).strip(), SEP_TAIL.sub('', e.group(2)).strip()))
                else:
                    rows.append((k, v))
                i += 1
            rows = [(k, v) for k, v in rows if v]
            out.append('<dl class="fields">' + ''.join(
                f'<dt>{inline(k)}</dt><dd>{inline(v)}</dd>' for k, v in rows) + '</dl>')
            continue

        buf = []
        while i < len(lines) and lines[i].strip() and not FIELD_LINE.match(lines[i]) and not re.match(
                r'^(#{1,6}\s|```|\||\s*[-*+]\s|\s*\d+[.)]\s|>|---+\s*$|\s*</?(details|summary)\b)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        if buf:
            out.append('<p>' + inline(' '.join(buf)) + '</p>')
        else:
            i += 1
    return '\n'.join(out), toc


PAGE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page_template.html')).read()

ACCENTS = {
    '02-pronouns': ('#2f6f6b', '#79c9c2'), '06-prepositions': ('#3f6b4a', '#7fc08d'),
    '07-conjunctions': ('#2f5d8a', '#79b0e8'), '08-interjections': ('#b4552a', '#e8935f'),
    '09-determiners': ('#7a4a86', '#c193cc'), '10-pronunciation': ('#8a6d2f', '#d6b76a'),
    'grammar': ('#9a4b52', '#e8919a'),
}


def accent_for(rel):
    for k, v in ACCENTS.items():
        if rel.startswith(k) or f'/{k}/' in rel:
            return v
    return ('#8a5a3b', '#d09b72')


def crumb_for(rel):
    depth = rel.count('/')
    up = '../' * depth
    parts = [f'<a href="{up}index.html">Learn English</a>']
    seg = rel.split('/')
    if seg[0] in ('parts-of-speech', 'grammar'):
        name = 'Parts of speech' if seg[0] == 'parts-of-speech' else 'Grammar'
        parts.append('<span class="sep">/</span>')
        parts.append(f'<a href="{"../"*(depth-1)}README.html">{name}</a>' if depth > 1 else f'<span>{name}</span>')
        if depth >= 2:
            parts.append('<span class="sep">/</span>')
            if depth == 2:
                parts.append(f'<span>{seg[1]}</span>')
            else:
                parts.append(f'<a href="{"../"*(depth-2)}README.html">{seg[1]}</a>')
                parts.append(f'<span class="sep">/</span><span>{seg[2]}</span>')
    elif seg[0] == '10-pronunciation':
        parts.append('<span class="sep">/</span><span>Pronunciation</span>')
    return ''.join(parts)


if __name__ == '__main__':
    built = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'tools', 'data')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            rel = posixpath.relpath(os.path.join(dirpath, fn), ROOT)
            src = open(os.path.join(ROOT, rel)).read()
            body, toc = convert(src)
            title = plain((re.search(r'^#\s+(.+)$', src, re.M) or [None, rel])[1])
            a, ad = accent_for(rel)
            toc_html = ''
            if len(toc) >= 6:
                items = ''.join(f'<a href="#{anc}">{html.escape(t)}</a>' for t, anc in toc)
                toc_html = f'<div class="toc"><b>On this page</b>{items}</div>'
            page = (PAGE.replace('__TITLE__', html.escape(title))
                        .replace('__ACCENT__', a).replace('__ACCENT_DARK__', ad)
                        .replace('__CRUMB__', crumb_for(rel))
                        .replace('__TOC__', toc_html)
                        .replace('__BODY__', body))
            open(os.path.join(ROOT, rel[:-3] + '.html'), 'w').write(page)
            built += 1
    print(f'rendered {built} markdown files to HTML')
