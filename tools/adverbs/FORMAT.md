# Entry format for the adverb dictionary

The adverb dictionary has two tiers, both written as JSON and rendered by
`tools/build_adverbs.py`, so nobody hand-edits the markdown.

- **Grammar tier** — `tools/adverbs/groups/<NN>-<slug>.json`. The adverbs that carry
  grammar: flat adverbs, irregular comparison, the *-ly* forms whose meaning drifted,
  and the closed sets of place, time, frequency, degree, focus, stance and linking.
  Every sense, and a contrast note wherever there is a trap.
- **Core tier** — `tools/adverbs/core/add-<NN>.json`. Everything else from a coverage
  check against WordNet's 4,481 adverb lemmas that survived a rejection pass —
  mostly *-ly* manner adverbs, plus the multi-word adverbs (*of course*, *by and large*).

Both use the same shape:

```json
[
  {
    "term": "hardly",
    "ipa": "ˈhɑːrdli",
    "respell": "HAHRD-lee",
    "ru": "едва, почти не",
    "type": "degree — a downtoner with negative force",
    "position": "mid — before the main verb, after *be* and the first auxiliary",
    "comparison": "not gradable",
    "modifies": "verbs, adjectives, adverbs, and quantifiers (*hardly anyone*)",
    "form": "-ly from *hard*, but not its meaning",
    "contrast": "Optional. Only for a real trap.",
    "senses": [
      {
        "gloss": "Almost not; only just.",
        "ru": "едва, почти не",
        "examples": [
          "I could *hardly* hear her over the music.",
          "We had *hardly* sat down when the lights went out.",
          "There's *hardly* any coffee left."
        ]
      }
    ]
  }
]
```

## The four label fields open with a fixed word

The browser turns the first clause of `type`, `position` and `comparison` into a filter
tag — everything before the first `—`, `(`, `;` or `,`. So each of those fields **must
open with one of the words below**, and any explanation goes after ` — `.

- **`type`** — `manner`, `place`, `direction`, `time`, `duration`, `frequency`, `degree`,
  `focusing`, `viewpoint`, `stance`, `linking`, `interrogative`, `relative`,
  `negative`, `particle`. A word with several jobs names its main one first and the
  rest after a semicolon: `time; also focusing and degree`.
- **`position`** — `front`, `mid`, `end`, `front or end`, `mid or end`,
  `any position`, `before its word` (degree adverbs before an adjective),
  `after its word` (*enough*, *ago*, *indeed* in *very good indeed*).
- **`comparison`** — `not gradable`, `more/most`, `-er/-est`, `irregular`, then the
  actual forms after ` — `: `-er/-est — *faster*, *fastest*`;
  `irregular — *better*, *best*`. Never a comma before the dash.
- **`modifies`** — free text, short: what the adverb can attach to.

## Hard rules

- **`ipa`** — General American, **no** slashes. *hot* /ɑː/ not /ɒ/; rhotic /ər/;
  **/ɛ/** for the DRESS vowel, never bare /e/ (bare /e/ belongs only to /eɪ/);
  /ɪr ɛr ʊr/ not /ɪə eə ʊə/; a diphthong before schwa keeps it (*finally*
  /ˈfaɪnəli/). The *-ly* ending is /li/.
- **`respell`** — stressed syllable in CAPITALS, syllables hyphenated, a space between
  words. Schwa `uh`; /ʊ/ `UU`; /uː/ `OO`; /ər/ `ur`; /ɜːr/ `UR`; /ɔːr/ `OR`;
  word-final /ɛr/ `AIR`; /aɪ/ `Y` (*FYN-uh-lee*). No silent final `-e`.
- **`ru`** — the Russian adverb or short equivalent. Not a sentence.
- **`form`** — how the word is built, when that helps: `-ly from *careful*`,
  `flat — the same form as the adjective *fast*`, `suppletive — the adverb of *good*`,
  `-ward — direction`. Omit for simple words (*soon*, *here*).
- **`senses`** — one object per **genuinely distinct** adverb meaning, **most common
  first**. *just* has at least four (exactly, only, a moment ago, barely); *still* has
  two unrelated ones (continuing; nevertheless). Do not split a sense because the
  context changes; do split it when the Russian translation changes.
- **`examples`** — natural American English, headword in single asterisks in every one.
  A single-sense entry has **exactly 3**; each sense of a multi-sense entry has
  **2 or 3**. When `comparison` is `-er/-est` or `irregular`, at least one example
  in the entry uses the comparative or superlative (*She drove **faster** than me*,
  asterisked as `*faster*`).
- **`contrast`** — omit unless there is a trap: a flat/*-ly* pair that means different
  things (*hard* / *hardly*), a position that changes the meaning (*only*), inversion
  after a fronted negative (*Never have I…*), a false friend for a Russian speaker, a
  US/UK split, or the same spelling working as a preposition or conjunction.

## Never

- **Only adverb uses.** *fast* in *a fast car* is an adjective; *up* in *up the hill*
  is a preposition; *well* meaning *healthy* is an adjective. Those senses belong to
  other dictionaries — mention them in `contrast` if they cause confusion, but do not
  write them as senses.
- No archaic, dialect or British-only adverb unless the `contrast` says so and it is
  still met in American reading.
- No invented pronunciations — if unsure of a word's IPA, drop the word.
- Single asterisks only, always balanced. Never `**bold**` inside examples.
