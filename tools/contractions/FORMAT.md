# Entry format for the contraction dictionary

Contractions are not a word class — *I'm* is a pronoun plus a verb, *won't* is a modal
plus *not* — so they live under `grammar/`, beside reported speech. Each group file is
`tools/contractions/groups/<NN>-<slug>.json`, a JSON array rendered by
`tools/build_contractions.py`.

```json
[
  {
    "term": "won't",
    "ipa": "woʊnt",
    "respell": "WOHNT",
    "ru": "не буду, не будет (сокращение от will not)",
    "expands": "*will not*",
    "type": "negative",
    "register": "standard — normal in speech and in all but the most formal writing",
    "question": "*Won't you come?* — the contracted form is the natural question; *Will you not come?* is stiff and marked.",
    "ambiguity": "Optional. What else the same string can stand for.",
    "contrast": "Optional. Only for a real trap.",
    "senses": [
      {
        "gloss": "The contraction of *will not*.",
        "ru": "не буду, не будет",
        "examples": [
          "I *won't* be at the meeting on Thursday.",
          "The car *won't* start in this cold.",
          "*Won't* you sit down?"
        ]
      }
    ]
  }
]
```

## The two label fields open with a fixed word

The browser turns the first clause of `type` and `register` into a filter tag —
everything before the first `—`, `(`, `;` or `,`.

- **`type`** — `be`, `have`, `had`, `will`, `would`, `negative`, `modal`, `informal`,
  `dialect`.
- **`register`** — `standard` (normal in speech and ordinary writing), `informal`
  (speech and casual writing only), `nonstandard` (widely used, marked as an error in
  school and formal writing — *ain't*), `regional` (*y'all*), `dated`.

## Hard rules

- **`expands`** — what the contraction stands for, in asterisks: `*will not*`. When it
  stands for more than one thing, list them: `*he is* or *he has*`.
- **`ipa`** — General American, **no** slashes. `/ɛ/` for the DRESS vowel, never bare
  `/e/`; `/ɑː/` not `/ɒ/`; rhotic `/ər/`. The pronunciation is the point of several of
  these entries: *won't* is /woʊnt/, not "will-not run together"; *can't* is /kænt/;
  the *-n't* of *isn't* is a syllabic /ən/.
- **`respell`** — stressed syllable in CAPITALS: `WOHNT`, `KANT`, `IZ-uhnt`.
- **`ru`** — what it means in Russian plus what it is short for. Not a sentence.
- **`question`** — only where the question form is a trap: *aren't I?*, *won't you?*,
  and the modals with no contracted question (*mayn't*).
- **`ambiguity`** — required whenever the written form is ambiguous: *'s* is *is* or
  *has* (and *us* in *let's*), *'d* is *would* or *had*, *it's* is never possessive.
- **`senses`** — one per distinct expansion. *he's* has two (*he is*, *he has*);
  *I'd* has two (*I would*, *I had*). Order: the commoner expansion first.
- **`examples`** — natural American English, the contraction in single asterisks in
  every one. A single-sense entry has **exactly 3**; each sense of a multi-sense entry
  has **2 or 3**. For an ambiguous form, at least one example must make the expansion
  unmistakable (*He's gone* = has; *He's tired* = is).
- **`contrast`** — the real traps: *it's* vs *its*, *they're* vs *their* vs *there*,
  *you're* vs *your*, *who's* vs *whose*, *could've* heard as "could of", the fact that
  a contraction cannot end a clause (*Yes, I am*, never ✗ *Yes, I'm*).

## Never

- No possessive *'s* — that is the noun dictionary's job, and the apostrophe means
  something else there.
- No invented forms: *amn't* and *mayn't* are not American English. Say so in
  `contrast` rather than writing an entry.
- Single asterisks only, always balanced. Never `**bold**` inside examples.
