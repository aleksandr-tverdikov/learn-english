# Build tools

The Markdown is the **single source of truth**. Everything else — the JSON, the A–Z indexes,
the audio browsers, and the whole HTML site — is generated from it.

```
python3 tools/build_all.py        # the whole pipeline, then verify
```

| Script | Writes |
|---|---|
| `build_browsers.py` | `<catalog>/browse.html`, `<catalog>/README.md`, `<catalog>/data/*.json` |
| `build_site.py` | one `.html` beside every `.md` |
| `build_home.py` | `index.html` (all counts read from disk, never hardcoded) |
| `check_links.py` | nothing — verifies every link, anchor, and `**` pair; exits non-zero on failure |

`lib.py` holds the shared parser, `catalogs.py` the list of dictionaries, and the two
`*_template.html` files the page shells.

## Adding a dictionary

Add one row to `catalogs.py` — path, title, accent color, and which markdown labels to
surface as fields — then run `build_all.py`. Nothing else needs changing: `build_home.py`
derives its dictionary cards from that list, and `check_links.py` picks up the new counts.
Optionally add a one-line blurb to `BLURBS` in `build_home.py` for the home-page card.

## Two things that are easy to get wrong

**Anchors.** GitHub turns *each* space into a hyphen and does not collapse runs, so a heading
like `as … as` becomes `as--as`. `slugify()` in `lib.py` matches that exactly. Collapsing the
runs silently breaks every anchor into a heading containing punctuation.

**Emphasis.** The corpus nests bold and italic five different ways (`**With *of***`,
`***That** book is mine*`, `*near **what we needed***`, `*the red **and** the blue*`,
`***through***`). The only ordering that survives all five is: tight `***x***`, then plain
bold, then bold-containing-italics, then italics. Special-casing each shape produces greedy
patterns that swallow whole paragraphs. `emphasis()` in `lib.py` is that ordering — change it
only with the five shapes in front of you.

Note that a leading `*` is also the linguistic convention for an ungrammatical example. This
library writes those as `✗ *like this*` rather than `**like this*`, which Markdown cannot
parse and which leaves the file with unbalanced `**`. `check_links.py` counts those.

**Field lines.** A dictionary entry is mostly `**Label:** value` lines. Plain Markdown — here
and on GitHub — merges consecutive lines into one paragraph, which turns an entry into an
unreadable wall of text. `build_site.py` therefore treats a run of those lines as a definition
list, and splits labels that share a line (`**Type:** x &middot; **Case:** y &middot; **Register:** z`)
into separate rows, the same way `build_browsers.py` does. If entries ever start reading as one
long string again, that block is the thing to check.
